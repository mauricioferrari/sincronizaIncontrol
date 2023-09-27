import datetime
import os

class logger:
    def __init__(self):
        data_atual = datetime.date.today()
        self.nome_arquivo = f"log_{data_atual}.txt"

    def escrever(self, texto):
        with open(self.nome_arquivo, 'a') as arquivo:
            arquivo.write(texto + '\n')