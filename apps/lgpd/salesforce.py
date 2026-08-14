import requests
import json
from core.settings import SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_DOMAIN
from apps.lgpd.utils import colocar_mascara_no_cpf_cpnj, cpf_adicionar_zero_a_esquerda

def salesforce_buscar_account_id_por_cpf(cpf):
    # TODO implementar a função 'salesforce_buscar_account_id_por_cpf'
    print("(salesforce) ")

# TODO implementar função para atualizar os campos do lgpd do participante na salesforce
def salesforce_atualizar_termo_aceite_lgpd_por_account_id(account_id, aceitar_lgpd=False):
    url = SALESFORCE_DOMAIN + "/services/data/v62.0/sobjects/Account/" + account_id
    payload = json.dumps({
      "TermoAceiteLGPD__c": "Sim" if aceitar_lgpd else "Não"
    })
    headers = {
      'Authorization': 'Bearer ' + salesforce_token(),
      'Content-Type': 'application/json',
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    if not response.ok:
        print("(salesforce) fatal error", response.text)
        return None
    if response.status_code == 204:
        return "OK"
    return None

def salesforce_token():
    url = SALESFORCE_DOMAIN + "/services/oauth2/token"
    payload = f'grant_type=client_credentials&client_id={SALESFORCE_CLIENT_ID}&client_secret={SALESFORCE_CLIENT_SECRET}'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
    }
    response = requests.post(url, headers=headers, data=payload)
    if not response.ok:
        print("(salesforce) fatal error", response.text)
    data = response.json()
    return data.get("access_token", None)

def salesforce_query(sql):
    if not sql:
        return None
    url = SALESFORCE_DOMAIN + "/services/data/v62.0/query/?q=" + sql
    headers = {
      'Authorization': 'Bearer ' + salesforce_token(),
      'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        print("(salesforce) fatal error", response.text)
    return response.json()

def salesforce_buscar_parceiro_por_cpf(cpf):
    if not cpf:
        return None
    if not isinstance(cpf, str):
        cpf = cpf_adicionar_zero_a_esquerda(cpf)
    cpf = colocar_mascara_no_cpf_cpnj(cpf)
    sql = f"""
    SELECT FIELDS(All) 
    FROM ACCOUNT 
    WHERE CPF__c != NULL 
    AND CPF__c = '{cpf}' 
    ORDER BY Name LIMIT 5
    """
    return salesforce_query(sql)
    
