from core.settings import PLIQ_TOKEN, FLAG_PLIQ_ENABLED, PLIQ_DOMAIN
import requests
import json
from datetime import datetime
import re

def pliq_buscar_pesquisas_respondidas():
    startdate = f"{datetime.now().year}-{'{:02d}'.format(datetime.now().month)}-{'{:02d}'.format(datetime.now().day)}"
    finishdat = f"{datetime.now().year}-{'{:02d}'.format(datetime.now().month)}-{'{:02d}'.format(datetime.now().day)}"
    url = f"{PLIQ_DOMAIN}/v2/api/surveys/feedbacks?survey_code=c922de9e01cba8a4684f6c3471130e4c&startedat={startdate}&finishedat={finishdat}&days=1"
    headers = {
      'PLIQ_TOKEN': PLIQ_TOKEN,
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        print("FATAL ERRO PLIQ", response.text)
        return None
    return response.json()

def pliq_cadastrar_contato(cpf, telefone, nome_razao_social=None):
    if not cpf or not telefone:
        return None
    if not nome_razao_social:
        nome_razao_social = cpf
    nome_razao_social = re.sub(r'[^a-zA-Z\s]', '', nome_razao_social)
    if FLAG_PLIQ_ENABLED:
        url = "https://sandbox-api.pliq.io/v2/api/import"
        payload = json.dumps({
          "nameImport": cpf,
          "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
          "update_import": 2,
          "baseLegal": 3,
          "fk_journey": 607,
          "customers": [
            {
              "name": nome_razao_social,
              "email": "vinicius.moura@acto.com.br",
              "phone": "55"+telefone,
              "identification": cpf,
              "state": "Mato Grosso do Sul",
              "tagsCustomer": [
                "Potencial Cliente",
                "Primeira Abordagem"
              ],
              "segment": "Tecnologia",
              "enterprise": "Empresa Teste LTDA",
              "register_number": "12345678000190",
              "comments": "Cliente em potencial para novos projetos",
              "key_attendance": "ATEND-2025-001",
              "ticket_media": 0,
              "start_contract": "2025-01-15",
              "last_name": "da Silva",
              "country": "Brasil",
              "region": "Centro-Oeste",
              "city": "Campo Grande",
              "neighborhood": "Centro",
              "address": "Rua Principal, 123",
              "cep": "79002-100",
              "complement": "Sala 501",
              "number": "123"
            }
          ],
          "flg_email": True,
          "flg_popup": False,
          "flg_whatsapp": True,
          "flg_sms": True
        })
        headers = {
          'PLIQ_TOKEN': PLIQ_TOKEN,
          'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        if not response.ok:
            print("FATAL ERROR", response.text)
            return None
        return response.json()
    return {'message': 'Import being carried out!'}

