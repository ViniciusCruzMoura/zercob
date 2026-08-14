import requests
from core.settings import SAS_X_REQ, SAS_DOMAIN

def sas_buscar_parceiro_por_codigo(cod_parceiro):
    url = f"{SAS_DOMAIN}/SasServiceCliente/Cliente/ConsultarPessoaFisica?CodSebrae=34&CodParceiro={cod_parceiro}"
    headers = {
      'x-req': SAS_X_REQ,
      'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        print("(sas) fatal error", response.text)
        return None
    return response.json()

def sas_buscar_parceiro_por_cpf(cpf):
    url = f"{SAS_DOMAIN}/SasServiceCliente/Cliente/ConsultarPessoaFisica?CodSebrae=34&CgcCpf={cpf}"
    headers = {
      'x-req': SAS_X_REQ,
      'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        print("(sas) fatal error", response.text)
        return None
    return response.json()
