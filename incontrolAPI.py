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
from pickle import FALSE
from time import sleep
import requests

#Parametros do servidor Incontrol {
usr="admin"
pwd="admin"
srv="172.32.1.22"
port="4441"
srvadd="http://" + srv + ":" + port
#}

#GERA O TOKEN UTILIZADO NAS TRANSAÇÕES DA API
def geratoken(usr,pwd,srvadd): 
    payload={
        "username":""+usr+"",
	    "password":""+pwd+""
    }
    tokenadd=(srvadd + "/v1/auth/")
    r = requests.post(tokenadd, json=payload)
    data = r.json()
    return(data['token'])
#}

# ENVIA USUÁRIOS PARA A API {
def enviausr(token,nome_completo,matricula):
    datetime_atuais = datetime.now()
    datetime_stamp= str("Criado via script em " + datetime_atuais.strftime('%d/%m/%Y'))
    
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
      "id": 1
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
        "Authorization":"JWT " + token
    }
    tokenusr=(srvadd + "/v1/usuario/")
    r = requests.post(tokenusr, headers=header_usr, json=payload_usr)
    data = r.json()
    return(data['data'])
#}

#RECEBE LISTA DE USUÁRIOS DA API {
def recebeusr(token):
    header_usr={
        "Content-Type":"application/json",
        "Authorization":"JWT " + token
    }
    tokenusr=(srvadd + "/v1/usuario/")
    r = requests.get(tokenusr, headers=header_usr)
    data = r.json()
    usrs=data['data']
    cnt=0
    pessoas={}
    while len(usrs)>cnt:
        matricula=(usrs[cnt]['matricula'])
        id=usrs[cnt]['id']
        nome_completo=usrs[cnt]['pessoa']['nome_completo']
        pessoas[matricula]={'id':id,'nome':nome_completo}
        cnt+=1
    return(pessoas)
    #}

#ENVIA CREDENCIAL PARA A API {
def enviacartao(token,id_pessoa,cartao):
    header_crt={
        "Content-Type":"application/json",
        "Authorization":"JWT " + token
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

    tokencrt=(srvadd + "/v1/credencial/")
    r = requests.post(tokencrt, headers=header_crt, json=payload_crt)
    data = r.json()
    return(data)
#}

#RECEBE CARTÕES CADASTRADOS NA API {
def recebecrt(token):
  header_usr={
      "Content-Type":"application/json",
      "Authorization":"JWT " + token
  }
  tokenusr=(srvadd + "/v1/credencial/")
  r = requests.get(tokenusr, headers=header_usr)
  data = r.json()
  crds=data['data']
  cnt=0
  usr_incontrol_id={}
  usr_incontrol=recebeusr(token)
  usr_incontrol_keys=usr_incontrol.keys()
  for each in usr_incontrol_keys:
        usr_incontrol_id[usr_incontrol[each]['id']]={'matricula':each,'nome_completo':usr_incontrol[each]['nome']}
  matriculaxcrt={}
  while len(crds)>=cnt:
    try:
      crds[cnt]['pessoa']['id']
    except:
      pass
    else:
      pessoa_id=int(crds[cnt]['pessoa']['id'])-3
      pessoa_nome=(crds[cnt]['pessoa']['nome_completo'])
      pessoa_matricula=usr_incontrol_id[pessoa_id]['matricula']
      cartao_id=(crds[cnt]['cartao']['id'])
      matriculaxcrt[pessoa_matricula]={'id':pessoa_id,'nome':pessoa_nome, 'cartao':cartao_id}
    cnt+=1 
  return(matriculaxcrt)

#RECEBE APENAS NUMERAÇÃO DOS CARTÕES
def recebecrtdec(token):
  header_usr={
      "Content-Type":"application/json",
      "Authorization":"JWT " + token
  }
  tokenusr=(srvadd + "/v1/credencial/")
  r = requests.get(tokenusr, headers=header_usr)
  data = r.json()
  crds=data['data']
  cnt=0
  cartoesdec={}
  while len(crds)>=cnt:
    try:
      crds[cnt]['pessoa']['id']
    except:
      pass
    else:
      pessoa_id=int(crds[cnt]['pessoa']['id'])-3
      cartao_id=(crds[cnt]['cartao']['id'])
      cartao_dec=(crds[cnt]['cartao']['codigo_decimal'])
      cartoesdec[cartao_dec]={'id':pessoa_id,'cartao':cartao_id}
    cnt+=1 
  return(cartoesdec)

#RECEBE CARTÕES CADASTRADOS, incluindo orfãos
def recebecrtcadastrados(token):
  header_usr={
      "Content-Type":"application/json",
      "Authorization":"JWT " + token
  }
  tokenusr=(srvadd + "/v1/credencial/")
  r = requests.get(tokenusr, headers=header_usr)
  data = r.json()
  crds=data['data']
  cnt=0
  usr_incontrol_id={}
  usr_incontrol=recebeusr(token)
  usr_incontrol_keys=usr_incontrol.keys()
  for each in usr_incontrol_keys:
        usr_incontrol_id[usr_incontrol[each]['id']]={'matricula':each,'nome_completo':usr_incontrol[each]['nome']}
  matriculaxcrt={}
  for todes in crds.keys():
    try:
      crds[todes]['pessoa']['id'] #<-------------------------- parei aqui. Rodar as pessoas e ver se tem cartões (Identificar orfãos)
    except:
      pass
    else:
      pessoa_id=int(crds[cnt]['pessoa']['id'])-3
      pessoa_nome=(crds[cnt]['pessoa']['nome_completo'])
      pessoa_matricula=usr_incontrol_id[pessoa_id]['matricula']
      cartao_id=(crds[cnt]['cartao']['id'])
      matriculaxcrt[pessoa_matricula]={'id':pessoa_id,'nome':pessoa_nome, 'cartao':cartao_id}
    cnt+=1 
  return(matriculaxcrt)

#REMOVE CARTÃO CADASTRADO {
def removecrt(crt):
  token=geratoken(usr,pwd,srvadd)
  header_removecrt={
      "Content-Type":"application/json",
      "Authorization":"JWT " + token
  }

  token_removecrt=(srvadd + "/v1/credencial/batch_delete")
  payload_removecrt={
    "ids": [crt]
  }

  r = requests.post(token_removecrt, headers=header_removecrt, json=payload_removecrt)
  data = r.json()
  print(str(data))
  return(0)



#REMOVE USUÁRIO DA API
def removeusuario(usuario):
  token=geratoken(usr,pwd,srvadd)
  header_removeusuario={
      "Content-Type":"application/json",
      "Authorization":"JWT " + token
  }
  token_removeusuario=(srvadd + "/v1/usuario/batch_delete")
  payload_removeusuario={
    "ids": [usuario]
  }

  r = requests.post(token_removeusuario, headers=header_removeusuario, json=payload_removeusuario)
  data = r.json()
  return(0)



tkn=geratoken(usr,pwd,srvadd)
crt_cad=recebecrtcadastrados(tkn)
print(crt_cad)