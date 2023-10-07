import time
import incontrolAPI
import wiegand
import sqlite
import acessoNetDB

api=incontrolAPI.incontrolAPI() #instancia a classe oepradora da API
database=sqlite.database()  #instancia a classe operadora do sqlite
catraca=acessoNetDB.acessoNetDB()   #instancia a classe de leitra da catraca
database.cleanTables()  #Limpa as tabelas
database.createTables() #Cria as tabelas

#--- LENDO CATRACA ---#
usuariosCatraca=catraca.lerUsuariosAtivos() #le os usuários da catraca
for each in usuariosCatraca:    #insere os usuários da catraca no sqlite
    print(database.insert(f"insert into acessoNet (matricula, nome, cartao_decimal, cartao_wiegand, id) values ('{each}','{usuariosCatraca[each]['nome']}','{usuariosCatraca[each]['cartao']}','{usuariosCatraca[each]['cartao_w']}','{usuariosCatraca[each]['ID']}')"))
catraca.close() #Encerra a conexão

#--- LENDO API ---#
api_pessoas=api.recebeusr() #Lendo usuários da API
for each in api_pessoas:    #Inserindo no sqlite(incontrolPessoas)
    print(database.insert(f"insert into incontrolPessoas (matricula,id_pessoa,nome,id_geral) values ('{each}','{api_pessoas[each]['id']}','{api_pessoas[each]['nome']}','{api_pessoas[each]['id_geral']}')"))
api_cartoes=api.recebecrt() #Lendo cartões da API
for each in api_cartoes:    #Inserindo no sqlite(incontrolCartoes)
    print(database.insert(f"insert into incontrolCartoes (id_cartao,cartao_decimal,id_pessoa, id_credencial) values ('{each}','{api_cartoes[each]['id_cartao']}','{api_cartoes[each]['id_pessoa']}','{api_cartoes[each]['id_credencial']}')"))

#--- REMOVER USUÁRIOS INATIVOS ---#
usuariosInativos=database.select(f"SELECT i.id_geral FROM incontrolPessoas i LEFT JOIN acessoNet a ON i.matricula = a.matricula WHERE a.matricula IS NULL")
id_usuario_remover=[]
for each in usuariosInativos:
    id_usuario_remover.append(int(each[0]))
    print(each[0])
if id_usuario_remover:
    print(api.removeusuario(id_usuario_remover))
else:
    print("Não há usuarios para remover")
    time.sleep(3)

#--- REMOVENDO CARTOES ORFAOS ---#
cartao_remover=database.select(f"select id_credencial from incontrolCartoes where id_pessoa='null'")
id_cartao_remover=[]
for each in cartao_remover:
    id_cartao_remover.append(int(each[0]))
    print(each[0])
    # id_cartao_remover_string = ""
    # id_cartao_remover_string = ",".join(id_cartao_remover)
if id_cartao_remover:
    print(api.removecrt(id_cartao_remover))
else:
    print("Não há cartoes para remover")
    time.sleep(3)

#--- CARREGAR NOVOS USUÁRIOS ---#
usuariosNovos=database.select(f"SELECT a.nome, a.matricula, a.cartao_decimal FROM acessoNet a LEFT JOIN incontrolPessoas i ON a.matricula = i.matricula WHERE i.matricula IS NULL")
for each in usuariosNovos:
    retorno=api.enviausr(str(each[0]),str(each[1]))
    api.enviacartao(retorno['pessoa']['id'],each[2])
print(database.cleanTables())

# #--- CARREGAR USUARIOS DA API NOVAMENTE ---#
# api_pessoas=api.recebeusr() #Lendo usuários da API
# for each in api_pessoas:    #Inserindo no sqlite(incontrolPessoas)
#     print(database.insert(f"insert into incontrolPessoas (matricula,id_pessoa,nome,id_geral) values ('{each}','{api_pessoas[each]['id']}','{api_pessoas[each]['nome']}','{api_pessoas[each]['id_geral']}')"))

# #--- CARREGAR CARTÕES DOS NOVOS USUARIOS ---###
# usuariosCartoesnovos=database.select(f"SELECT matricula, nome, id_pessoa from incontrolPessoas")
# for each in usuariosCartoesnovos:
#     print(each)

# # print(database.dropTable('stocks'))
# # print(database.listTable())
# # print(database.insert("insert into incontrol(matricula,id_pessoa,nome, id_cartao, cartao_decimal) values ('181512','13','Mauricio Ferrari','15','15161889')"))
# print(database.select("select * from incontrolPessoas"))
# print(database.select("select * from incontrolCartoes where id_pessoa = 'null'"))
