import sqlite3
import datetime
import os

# Se o arquivo não existir ele cria e conecta, senão só conecta
con = sqlite3.connect('data.db')
cur = con.cursor()

# Cria a tabela no banco de dados do arquivo acima se a tabela não existir
cur.execute('''CREATE TABLE IF NOT EXISTS stocks
               (date text, trans text, symbol text, qty real, price real)''')

# Esse bloco do código eu criei só pra caso você rodar o script mais de uma vez
# ele só insere os dados se o arquivo /tmp/insertok não existir e cria o arquivo
# Só insere os dados se o arquivo /tmp/insertok não existir 
if os.path.isfile('datacontrol.db'):
    print("", end ="")
else:
    cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    f = open("datacontrol.db", "a")
    f.write("insertok")
    f.close()

# valida as alterações feitas
con.commit()

# Seleciona os dados da tabela do banco de dados e imprime na tela
for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
    print(row[0])
    data = row[0] # criei isso só para formatar a saída para dd/mm/yyyy
    print(row[1])
    print(row[2])
    print(row[3])
    print(row[4])
    #print(row)
con.close()

# formtando a data
output = datetime.datetime.strptime(data, '%Y-%m-%d')
print(output.date().strftime("%d/%m/%Y"))