import sqlite3
import datetime
import os

class database:
    def __init__(self):
        # Se o arquivo não existir ele cria e conecta, senão só conecta
        self.con = sqlite3.connect('data.db')
        self.cur = self.con.cursor()

    def select(self,query):
        try:
            self.cur.execute(f'{query}')
        except sqlite3.IntegrityError as e:
            return(f"Erro: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Erro: {e}")
        else:
            return(self.cur.fetchall())

    def insert(self,query):
        print(f'{query}')
        try:
            self.cur.execute(f'{query}')
            self.con.commit()
        except sqlite3.IntegrityError as e:
            # Lidar com a violação de integridade (por exemplo, chave duplicada)
            return(f"Erro: {e}")
            # Você pode reverter ou desfazer as alterações aqui, se necessário
        except sqlite3.DatabaseError as e:
            # Lidar com outros erros do banco de dados
            return(f"Erro: {e}")
        else:
            return("OK")
    
    def update(self,query):
        try:
            self.cur.execute(f'{query}')
            self.con.commit()
        except sqlite3.IntegrityError as e:
            # Lidar com a violação de integridade (por exemplo, chave duplicada)
            return(f"Erro: {e}")
            # Você pode reverter ou desfazer as alterações aqui, se necessário
        except sqlite3.DatabaseError as e:
            # Lidar com outros erros do banco de dados
            return(f"Erro: {e}")
        else:
            return("OK")

    def delete(self,query):
        try:
            self.cur.execute(f'{query}')
            self.con.commit()
        except sqlite3.IntegrityError as e:
            # Lidar com a violação de integridade (por exemplo, chave duplicada)
            return(f"Erro: {e}")
            # Você pode reverter ou desfazer as alterações aqui, se necessário
        except sqlite3.DatabaseError as e:
            # Lidar com outros erros do banco de dados
            return(f"Erro: {e}")
        else:
            return("OK")
    
    def dropTable(self, table):
        try:
            # Execute a operação DROP TABLE para excluir a tabela 'table'
            self.cur.execute(f'DROP TABLE IF EXISTS {table}')
            self.con.commit()
        except sqlite3.OperationalError as e:
            return(f"Erro: {e}")
            # Trate a falta de existência da tabela ou problemas de permissão aqui
        except sqlite3.DatabaseError as e:
            return(f"Erro: {e}")
            # Lidar com erros gerais do banco de dados aqui
        else:
            return("OK")
    
    def listTable(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Recupere os resultados usando fetchall() ou fetchone()
        return(self.cur.fetchall())
    
    def cleanTables(self):
        try:
            self.dropTable("incontrolPessoas")
            self.dropTable("incontrolCartoes")
            self.dropTable("acessoNet")
            # valida as alterações feitas
            self.con.commit()
        except:
            return(f"Erro")
        else:
            return(f"OK")
        
    def createTables(self):
        # Cria a tabela no banco de dados do arquivo acima se a tabela não existir
        self.cur.execute('''CREATE TABLE IF NOT EXISTS incontrolPessoas
               (matricula text, id_pessoa text, nome text, id_geral)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS incontrolCartoes
               (id_cartao text, cartao_decimal text, id_pessoa text, id_credencial text)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS acessoNet
               (matricula text, nome text, cartao_decimal text, cartao_wiegand text, id text)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS controle
               (status text)''')
        # valida as alterações feitas
        self.con.commit()

        
    def close(self):
        self.con.close()