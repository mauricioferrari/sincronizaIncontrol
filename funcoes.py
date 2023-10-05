import json
import pathlib
import time
import incontrolAPI
import logger
import acessoNetDB



def removerUsuarios():
       #definições
    log=logger.logger()
    dbCreds=lerCred()

    #Credenciais
    usr=str(dbCreds["username"])
    pwd=str(dbCreds["password"])
    srv=str(dbCreds["srv"])
    port=str(dbCreds["port"])
    srvadd="http://" + srv + ":" + port

    log.escrever('Inicializando Remoção de Usuários')
    #verificar se arquivo db existe, se existe cria backup, se não, cria o arquivo

    log.escrever('Lendo usuários do arquivo DB')
    usr_catraca=acessoNetDB.lerUsuariosAtivos()
    log.escrever('Lendo usuários da DB da Catraca')
    token=incontrolAPI.geratoken(usr,pwd,srvadd)
    log.escrever('Gerando Token da API Incontrol')
    crt_incontrol=incontrolAPI.recebecrt(token)
    log.escrever('Recebendo cartões da API Incontrol')
    crt_dec_incontrol=incontrolAPI.recebecrtdec(token)
    log.escrever('Recebendo decimais de cartões da API Incontrol')
    usr_incontrol=incontrolAPI.recebeusr(token)
    log.escrever('Recebendo usuários da API Incontrol')

    mat_incontrol=usr_incontrol.keys()

    for each in mat_incontrol:  #Verifica se usuário está na catraca e o exclui
        try:
            usr_catraca[each]
        except KeyError:
            log.escrever('O usuário ' + str(each) + ' não foi localizado na catraca, iniciar exclusão')
            # incontrolAPI.removecrt(crt_incontrol[each]['cartao'])
            try:
                print("TENTANDO REMOVER USUARIO"+str(crt_incontrol[each]['id']))
            except:
                pass                
            try:
                incontrolAPI.removeusuario(int(crt_incontrol[each]['id']))
            except:
                pass
            try:
                print("TENTANDO REMOVER CARTÃO"+str(crt_incontrol[each]['cartao']))
            except:
                pass     
            try:
                incontrolAPI.removecrt(int(crt_incontrol[each]['cartao']))
            except:
                pass
        else:
            log.escrever('O usuário ' + str(each) + ' está OK')
    cartoes_catraca={}
    cartoes_incontrol=crt_dec_incontrol.keys()
    for all in usr_catraca.keys():
        cartoes_catraca[str(usr_catraca[all]['cartao'])]={}
    for any in cartoes_incontrol:
        try:
            cartoes_catraca[str(any)]
        except KeyError:
            print("TENTANDO REMOVER CARTÃO"+str(crt_dec_incontrol[any]['cartao']))
            incontrolAPI.removecrt(int(crt_dec_incontrol[any]['cartao']))
            print("TENTANDO REMOVER usuario"+str(crt_dec_incontrol[any]['id']))
            incontrolAPI.removeusuario(int(crt_dec_incontrol[any]['id']))
            log.escrever('O usuário com ID ' + str(crt_dec_incontrol[any]['id']) + ' foi removido! Cracha Alterado ou excluido na catraca.')
            time.sleep(0.5)
        else:
            pass

removerUsuarios()