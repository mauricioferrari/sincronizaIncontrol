import incontrolAPI
import deletaIncontrol
import acessoNetDB
import logger

#Credenciais
usr="admin"
pwd="admin"
srv="172.32.1.22"
port="4441"
srvadd="http://" + srv + ":" + port

deletaIncontrol.vai() #Deleta usuários do Incontrol antes de inserir novos

dados_catraca=acessoNetDB.lerUsuariosAtivos()
token=incontrolAPI.geratoken(usr,pwd,srvadd)
dados_api=incontrolAPI.recebeusr(token)

subir_credencial=[]
usr_catraca=dados_catraca.keys()
for each in usr_catraca:
    try:
        dados_api[each]
    except KeyError:
        incontrolAPI.enviausr(token,dados_catraca[each]['nome'],each)
        subir_credencial.append(each)
        logger.lognow("wherelog", 'Enviando usuario ' + str(dados_catraca[each]['nome'] + " - "+ str(each)))

dados_api=incontrolAPI.recebeusr(token)
for aaa in subir_credencial:
    id_incontrol=int(dados_api[aaa]['id'])+3
    incontrolAPI.enviacartao(token,id_incontrol,dados_catraca[aaa]['cartao'])
    logger.lognow("wherelog", 'Enviando credencial' + id_incontrol,dados_catraca[aaa]['cartao'] + " para ID de usuario calculado "+ str(id_incontrol))

