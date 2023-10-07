import time
import pyodbc
import wiegand

class acessoNetDB:
    def __init__(self): #inicia a conexao
        conexaoDB = (
            "Driver={SQL Server};"
            "Server=172.32.1.22\SQLEXPRESS1;"
            "Database=SecullumAcessoNet2;"
            "UID=integracao;"
            "PWD=Pelotassss-1"
        )
        try:
            self.conexao = pyodbc.connect(conexaoDB)
            self.cursor = self.conexao.cursor()
        except pyodbc.Error as e:
            raise (f"Falha ao Conectar: {e}")
        except Exception as ex:
            raise (f"Ocorreu um erro inesperado: {ex}")
        except:
            raise (f"Erro Genérico")
        
    def lerUsuariosAtivos(self):
        self.cursor.execute("SELECT [n_folha] as matricula ,[id] ,[n_identificador] as cracha ,[nome] FROM [SecullumAcessoNet2].[dbo].[pessoas] WHERE [estado]=0;") 
        data = self.cursor.fetchall() 
        acessoNetAtivos={}
        for each in data:
            acessoNetAtivos[each[0]]={
                'nome':str(each[3]),
                'cartao':str(wiegand.decodificaWiegand(each[2])),
                'cartao_w':each[2],
                'ID': each[1]}
        return(acessoNetAtivos)

    def desativarLista(self, idDesativar):
        try:
            for any in idDesativar: 
                self.cursor.execute("UPDATE dbo.pessoas SET estado=3  WHERE id ="+ str(any) +";") 
                self.conexao.commit()
        except:
            return(f'Erro')
        else:
            return(f'OK')

    def close(self): #Encerra a conexao
        self.cursor.close()
        self.conexao.close()