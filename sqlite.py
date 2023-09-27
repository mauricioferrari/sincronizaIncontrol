import sqlite3
import datetime
import os

class database:
    def __init__(self):
        # Se o arquivo não existir ele cria e conecta, senão só conecta
        self.con = sqlite3.connect('data.db')
        self.cur = self.con.cursor()
        # Cria a tabela no banco de dados do arquivo acima se a tabela não existir
        self.cur.execute('''CREATE TABLE IF NOT EXISTS stocks
               (date text, trans text, symbol text, qty real, price real)''')

        self.cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
        self.f = open("datacontrol.db", "a")
        self.f.write("insertok")
        self.f.close()

        # valida as alterações feitas
        self.con.commit()

        # Seleciona os dados da tabela do banco de dados e imprime na tela
        for row in self.cur.execute('SELECT * FROM stocks ORDER BY price'):
            print(row[0])
            data = row[0] # criei isso só para formatar a saída para dd/mm/yyyy
            print(row[1])
            print(row[2])
            print(row[3])
            print(row[4])
            print(row)
        self.con.close()

        # formtando a data
        output = datetime.datetime.strptime(data, '%Y-%m-%d')
        print(output.date().strftime("%d/%m/%Y"))

db=database()