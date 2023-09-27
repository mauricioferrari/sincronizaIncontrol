import json
import pathlib
import incontrolAPI

def lerCred():
    # Abra o arquivo JSON para leitura
    with open('jcred.json', 'r') as arquivo_json:
        # Use a função load para carregar o JSON em um dicionário
        credenciais = json.load(arquivo_json)  #Armazena as credencias em um dicionario
    return(credenciais)

def removerUsuarios():
       #definições
    whereiam=pathlib.Path().resolve() #resolve o caminho atual
    wherelog=str(whereiam)+'\log.txt'   #cria caminho de log
    print(wherelog)

    #Credenciais
    usr="admin"
    pwd="admin"
    srv="172.32.1.22"
    port="4441"
    srvadd="http://" + srv + ":" + port

    logger.lognow(wherelog, 'Inicializando Remoção de Usuários')
    #verificar se arquivo db existe, se existe cria backup, se não, cria o arquivo

    logger.lognow(wherelog, 'Lendo usuários do arquivo DB')
    usr_catraca=acessoNetDB.lerUsuariosAtivos()
    logger.lognow(wherelog, 'Lendo usuários da DB da Catraca')
    token=incontrolAPI.geratoken(usr,pwd,srvadd)
    logger.lognow(wherelog, 'Gerando Token da API Incontrol')
    crt_incontrol=incontrolAPI.recebecrt(token)
    logger.lognow(wherelog, 'Recebendo cartões da API Incontrol')
    crt_dec_incontrol=incontrolAPI.recebecrtdec(token)
    logger.lognow(wherelog, 'Recebendo decimais de cartões da API Incontrol')
    usr_incontrol=incontrolAPI.recebeusr(token)
    logger.lognow(wherelog, 'Recebendo usuários da API Incontrol')

    mat_incontrol=usr_incontrol.keys()

    for each in mat_incontrol:  #Verifica se usuário está na catraca e o exclui
        try:
            usr_catraca[each]
        except KeyError:
            logger.lognow(wherelog, 'O usuário ' + str(each) + ' não foi localizado na catraca, iniciar exclusão')
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
            logger.lognow(wherelog, 'O usuário ' + str(each) + ' está OK')
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
            logger.lognow(wherelog, 'O usuário com ID ' + str(crt_dec_incontrol[any]['id']) + ' foi removido! Cracha Alterado ou excluido na catraca.')
            time.sleep(2)
        else:
            pass