#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Criado Por: Mauricio Ferrari
# E-mail: mauricio.ferrari@outlook.com
# Created Date: 06/2022
# version =1.0
# ---------------------------------------------------------------------------
""" Modulo de integração com a API Intelbras Incontrol para ações básicas"""  
# ---------------------------------------------------------------------------
from datetime import datetime
import json
from pickle import FALSE
from time import sleep
import requests
import wiegand

class incontrolAPI:
  def __init__(self):
    self.credenciais=self.lerCred()
    self.credenciais["apiserver"]="https://"+str(self.credenciais["srv"])+":"+str(self.credenciais["port"])
    self.token=self.geratoken()

  def lerCred(self):
      # Abra o arquivo JSON para leitura
      with open('jcred.json', 'r') as arquivo_json:
          # Use a função load para carregar o JSON em um dicionário
          credenciais = json.load(arquivo_json)  #Armazena as credencias em um dicionario
          print(credenciais)
      return(credenciais)

  #GERA O TOKEN UTILIZADO NAS TRANSAÇÕES DA API
  def geratoken(self):
      payload={
          "username":""+self.credenciais["username"]+"",
        "password":""+self.credenciais["password"]+""
      }
      tokenadd=(self.credenciais["apiserver"] + "/v1/auth/")
      r = requests.post(tokenadd, json=payload, verify=False)
      data = r.json()
      return(data['token'])
  #}

  # ENVIA USUÁRIOS PARA A API {
  def enviausr(self,nome_completo,matricula):
      datetime_atuais = datetime.now()
      datetime_stamp= str("Criado via script em " + str(datetime_atuais.strftime('%d/%m/%Y')))
      
      payload_usr={
    "pessoa": {
      "nome_completo": nome_completo,
      "cpf": "",
      "rg": "",
      "telefone_celular": "",
      "email": "",
      "veiculo": {
        "placa_numero": "",
        "placa_letra": "",
        "marca": {
          "id": ""
        },
        "cor": "",
        "modelo": ""
      },
      "grupo": {
        "id": 999999
      }
    },
    "departamento": {
      "id": 1
    },
    "matricula": matricula,
    "tipo_usuario": {
      "id": "N"
    },
    "estado": True,
    "data_contratacao": "" ,
    "data_demissao": "" ,
    "observacoes": datetime_stamp,
    "campos_personalizados": {
      "campo_1": ""
    }
  }

      header_usr={
          "Content-Type":"application/json",
          "Authorization":"JWT " + self.token
      }
      tokenusr=(self.credenciais["apiserver"] + "/v1/usuario/")
      try:
        r = requests.post(tokenusr, headers=header_usr, json=payload_usr, verify=False)
        data = r.json()
      except requests.exceptions.RequestException as e:
        return(f"Erro na solicitação: {e}")
      except:
        return("Erro")
      else:
        return(data['data'])
  #}

  #RECEBE LISTA DE USUÁRIOS DA API {
  def recebeusr(self):
      header_usr={
          "Content-Type":"application/json",
          "Authorization":"JWT " + self.token
      }
      tokenusr=(self.credenciais["apiserver"] + "/v1/usuario/")
      r = requests.get(tokenusr, headers=header_usr, verify=False)
      data = r.json()
      pessoas={}
      for each in data["data"]:
        pessoas[each['matricula']]={
            'id':each['pessoa']['id'],
            'nome':each["pessoa"]["nome_completo"],
            'id_geral':each["id"]
            }
      return(pessoas)
      #}

  #ENVIA CREDENCIAL PARA A API {
  def enviacartao(self,id_pessoa,cartao):
      header_crt={
          "Content-Type":"application/json",
          "Authorization":"JWT " + self.token
      }

      payload_crt={
    "nivel": {
      "id": "N"
    },
    "tipo": {
      "id": "CT"
    },
    "cartao": {
      "id": "",
      "codigo_hexa": "",
      "codigo_decimal": str(cartao),
      "tamanho": {
        "id": "26",
      }
    },
    "pessoa": {
      "id": int(id_pessoa)
    },
    "coacao": False,
    "admin": False
      }

      tokencrt=(self.credenciais["apiserver"] + "/v1/credencial/")
      r = requests.post(tokencrt, headers=header_crt, json=payload_crt, verify=False)
      data = r.json()
      return(data)
  #}

  #RECEBE CARTÕES CADASTRADOS NA API {
  def recebecrt(self):
    header_usr={
        "Content-Type":"application/json",
        "Authorization":"JWT " + self.token
    }
    tokenusr=(self.credenciais["apiserver"] + "/v1/credencial/")
    r = requests.get(tokenusr, headers=header_usr, verify=False)
    data = r.json()

    credenciais={}
    for each in data["data"]:
       credenciais[each["cartao"]["codigo_decimal"]]={
          'id_cartao':each["cartao"]["id"], 
          'id_pessoa': each["pessoa"]["id"] if (each["pessoa"] != None) else 'null', 
          'id_credencial': each["id"]
       }
    return(credenciais)

  #REMOVE CARTÃO CADASTRADO {
  def removecrt(self,crt):

    header_removecrt={
        "Content-Type":"application/json",
        "Authorization":"JWT " + self.token
    }

    token_removecrt=(self.credenciais["apiserver"] + "/v1/credencial/batch_delete")
    payload_removecrt={
      "ids": crt
    }
    print(payload_removecrt)
    try:
      r = requests.post(token_removecrt, headers=header_removecrt, json=payload_removecrt, verify=False)
      data = r.json()
    except requests.exceptions.RequestException as e:
      return(f"Erro na solicitação: {e}")
    except :
      return("Erro")
    else:
      return("OK")

  #REMOVE USUÁRIO DA API
  def removeusuario(self,usuarios):
    header_removeusuario={
        "Content-Type":"application/json",
        "Authorization":"JWT " + self.token
    }
    token_removeusuario=(self.credenciais["apiserver"] + "/v1/usuario/batch_delete")
    payload_removeusuario={
      "ids": usuarios
    }
    try:
      r = requests.post(token_removeusuario, headers=header_removeusuario, json=payload_removeusuario, verify=False)
      data = r.json()
    except requests.exceptions.RequestException as e:
      return(f"Erro na solicitação: {e}")
    except:
      return("Erro")
    else:
      return(data)

