from time import sleep
from unicodedata import decimal

def decodificaWiegand(cracha):
    #print ("Converter o crachá " + cracha)  #Perfumaria

    if len(cracha) > 8 or len(cracha) < 7:  #Varifica tamanho da variável cracha
        #print("Crachá Inválido")
        return(00000000)

    if len(cracha) == 7:    #Analisa tamanho da variável cracha (7 ou 8 digitos)
        temp=2
    else:
        temp=3

    id_acesso = cracha[temp: ]    #Extrai numeracao acesso
    id_identificacao = cracha[:temp] #Extrai numeracao identificacao

    #print (id_acesso)   #Perfumaria
    #print (id_identificacao) #Perfumaria

    id_acesso_bin=bin(int(id_acesso))   #Converte numeracao de acesso para bin
    id_acesso_bin=id_acesso_bin.lstrip('0b')    #Remove Identificador binario "0b"
    if len(id_acesso_bin)<16:   #Avalia se o binario tem 16 digitos
        add_zero_acesso=16-len(id_acesso_bin)   #Verifica quantos zeros são encessários para completar 16 bits
        #print (add_zero_acesso) #Perfumaria
        acesso_bin_str = str(id_acesso_bin) #Converter valor para string
        acesso_bin_str = acesso_bin_str.zfill(16) #completa a string com os zeros faltantes
    else:
        acesso_bin_str = str(id_acesso_bin)
    #print (id_acesso_bin)   #Perfumaria
    #print (acesso_bin_str)  #Perfumaria
    #print(len(id_acesso_bin))   #Perfumaria

    id_identificacao_bin=bin(int(id_identificacao)) #Converte numeracao de identificacao para bin
    id_identificacao_bin=id_identificacao_bin.lstrip('0b')    #Remove Identificador binario "0b"
    if len(id_identificacao_bin)<8:   #Avalia se o binario tem 8 digitos
        add_zero_identificacao=8-len(id_identificacao_bin)   #Verifica quantos zeros são encessários para completar 16 bits
        #print (add_zero_identificacao) #Perfumaria
        identificacao_bin_str = str(id_identificacao_bin) #Converter valor para string
        identificacao_bin_str = identificacao_bin_str.zfill(8) #completa a string com os zeros faltantes
    else:
        identificacao_bin_str = str(id_identificacao_bin)
    #print (id_identificacao_bin)    #Perfumaria
    #print (identificacao_bin_str)  #Perfumaria
    #print(len(id_identificacao_bin))    #Perfumaria

    binario_cracha=(identificacao_bin_str + acesso_bin_str) #Concatenar os binarios de acesso e identificacao
    #print(binario_cracha)   #Perfumaria
    #print(len(binario_cracha))  #Perfumaria
    decimal_cracha = int(binario_cracha, 2) #Converter Binario do crachá para decimal
    #print(decimal_cracha)   #Perfumaria
    return(decimal_cracha)  #Retorna valor
