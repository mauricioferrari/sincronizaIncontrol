import time
import pyodbc
import wiegand

conexaoDB = (
    "Driver={SQL Server};"
    "Server=172.32.1.22\SQLEXPRESS1;"
    "Database=SecullumAcessoNet2;"
    "UID=integracao;"
    "PWD=Pelotassss-1"
)

conexao=""
cursor=""


def init(): #inicia a conexao
    global conexao
    global cursor
    try:
        conexao = pyodbc.connect(conexaoDB)
    except pyodbc.Error as e:
        return(f"Falha ao Conectar: {e}")
    except Exception as ex:
        return(f"Ocorreu um erro inesperado: {ex}")
    except:
        return(f"erro")
    else: 
        initStatus="Conectado com Sucesso a SecullumAcessoNet2"
    cursor = conexao.cursor()
    return(initStatus)
    


def close(): #Encerra a conexao
    global conexao
    global cursor
    cursor.close()
    conexao.close()
    cursor=""
    conexao=""

def lerUsuariosAtivos():
    initStatus=init()
    global cursor
    cursor.execute("SELECT [n_folha] as matricula ,[id] ,[n_identificador] as cracha ,[nome] FROM [SecullumAcessoNet2].[dbo].[pessoas] WHERE [estado]=0;") 
    row = cursor.fetchone() 
    acessoNetAtivos=dict()
    while row: 
        acessoNetAtivos[row[0]]={
            'nome':str(row[3]),
            'cartao':str(wiegand.decodificaWiegand(row[2])),
            'cartao_w':row[2],
            'ID': row[1]}
        row = cursor.fetchone()
    close()
    print(initStatus)
    return(acessoNetAtivos)

def desativarLista(idDesativar):
    initStatus=init()
    global cursor
    global conexao
    # cursor.execute("UPDATE dbo.pessoas SET estado=3 WHERE id =4;")
    # conexao.commit()
    try:
        for any in idDesativar: 
            cursor.execute("UPDATE dbo.pessoas SET estado=3  WHERE id ="+ str(any) +";") 
            conexao.commit()
    except:
        print("Falha ao excluir!")
    close()
    print(initStatus)
    return(0)
