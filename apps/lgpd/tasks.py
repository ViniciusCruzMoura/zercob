from celery import shared_task
import requests
import json
import requests
from core.settings import PLIQ_TOKEN
from apps.lgpd.pliq import pliq_buscar_pesquisas_respondidas
from apps.lgpd.models import SebraeParceiro
from apps.lgpd.salesforce import salesforce_atualizar_termo_aceite_lgpd_por_account_id
from datetime import datetime

@shared_task(name='Task-Sincroniza-LGPD-Aceitos')
def task_atualizar_lgpd():
    # TODO buscar todas as pesquisas respondidas com sim ou nao, e atualizar o banco com a resposta
    print("Task-Sincroniza-LGPD-Aceitos")
    respostas = pliq_buscar_pesquisas_respondidas()
#     respostas = [
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019769.0,
#             #"participant_key": "5567991385043",
#             "participant_key": "5522999254680",
#             "abandonment": False,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "71717706134",
#             "name_key": "phone",
#             "respondedat": "2025-09-06T01:46:34.525015",
#             "createdat": "2025-09-06T01:46:34.525015",
#             "sendedat": None,
#             "tags": "{\"Tags\": [\"Potencial Cliente\", \"Primeira Abordagem\"]}",
#             "tagsList": {
#                 "Tags": [
#                     "Potencial Cliente",
#                     "Primeira Abordagem"
#                 ]
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740826.0,
#             "key_attendance": "ATEND-2025-001",
#             "comments": "Cliente em potencial para novos projetos",
#             "properties": None,
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": "sim",
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-06 01:46:33"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019768.0,
#             "participant_key": "5567991385043",
#             "abandonment": False,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "71717706134",
#             "name_key": "phone",
#             "respondedat": "2025-09-06T01:42:00.831534",
#             "createdat": "2025-09-06T01:42:00.831534",
#             "sendedat": None,
#             "tags": "{\"Tags\": [\"Potencial Cliente\", \"Primeira Abordagem\"]}",
#             "tagsList": {
#                 "Tags": [
#                     "Potencial Cliente",
#                     "Primeira Abordagem"
#                 ]
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740825.0,
#             "key_attendance": "ATEND-2025-001",
#             "comments": "Cliente em potencial para novos projetos",
#             "properties": None,
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": "não",
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-06 01:42:00"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019759.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T10:40:01.590005",
#             "createdat": "2025-09-05T10:40:01.590004",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 10:36:22"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019758.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T10:33:11.948737",
#             "createdat": "2025-09-05T10:33:11.948736",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 10:32:39"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019757.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T09:57:12.270308",
#             "createdat": "2025-09-05T09:57:12.270307",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 09:56:10"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019756.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T09:56:08.523586",
#             "createdat": "2025-09-05T09:56:08.523585",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 09:22:39"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019755.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T09:22:38.43616",
#             "createdat": "2025-09-05T09:22:38.43616",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 09:21:53"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019754.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T09:21:16.775416",
#             "createdat": "2025-09-05T09:21:16.775415",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 09:20:58"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019753.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T09:20:13.597118",
#             "createdat": "2025-09-05T09:20:13.597117",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 09:13:42"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019752.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T08:58:21.150121",
#             "createdat": "2025-09-05T08:58:21.150121",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 08:57:56"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019750.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T08:37:18.656561",
#             "createdat": "2025-09-05T08:37:18.65656",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 03:51:05"
#                 }
#             ],
#             "contact": None
#         },
#         {
#             "id_company": 790.0,
#             "full_name": "SebraeMS Sandbox",
#             "id_survey": 3130.0,
#             "url_survey": "c922de9e01cba8a4684f6c3471130e4c",
#             "type_survey": 3.0,
#             "type_survey_label": "Customizado",
#             "fk_survey_sample": 48.0,
#             "title": "TERMO DE CONSENTIMENTO (LGPD)",
#             "description": "Preencha a pesquisa para ajudar nossa empresa.",
#             "id_survey_response": 1019749.0,
#             "participant_key": "tech@pliq.com.br",
#             "abandonment": True,
#             "closed_loop": False,
#             "feedback_blocked": False,
#             "name": "Tech PliQ",
#             "name_key": "email",
#             "respondedat": "2025-09-05T08:33:25.779255",
#             "createdat": "2025-09-05T08:33:25.779254",
#             "sendedat": None,
#             "tags": "{\"Tags\": \"\"}",
#             "tagsList": {
#                 "Tags": ""
#             },
#             "referral_share_code": None,
#             "nps_value": 0,
#             "nps_feedback": "",
#             "anonymous": False,
#             "timezone": -3,
#             "fk_survey_audience": 740008.0,
#             "key_attendance": None,
#             "comments": None,
#             "properties": [
#                 {
#                     "value": None,
#                     "id_property": 235.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 236.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 237.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 238.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 239.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 240.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 241.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 242.0
#                 },
#                 {
#                     "value": None,
#                     "id_property": 243.0
#                 }
#             ],
#             "responses": [
#                 {
#                     "fk_question": 46361,
#                     "value": None,
#                     "fk_type_question": 5,
#                     "answers": None,
#                     "data_response": "2025-09-05 00:54:15"
#                 }
#             ],
#             "contact": None
#         }
#     ]
    for resposta in respostas:
        if not resposta.get("responses", [])[0].get("value", "não"):
            continue
        print("(task) Iniciado Integração Pliq ")
        telefone = resposta.get("participant_key").replace("55", "") if resposta.get("participant_key") else ""
        aceite_lgpd = True if resposta.get("responses")[0]["value"] in ["sim"] else False
        print("(task) Telefone ::", telefone, ":: aceite_lgpd ::", aceite_lgpd)

        # TODO buscar pelo CPF ao inves do telefone, mas a pliq não retorna o CPF
        obj = SebraeParceiro.objects.filter(numero=telefone).first()
        print("(task) esta importado o parceiro?", True if obj else False)

        if not obj:
            continue
        print("(task) já esta aceito o termo ?", True if obj.termo_aceite_lgpd else False)
        if obj.termo_aceite_lgpd:
            continue

        obj.termo_aceite_lgpd = aceite_lgpd
        foco = salesforce_atualizar_termo_aceite_lgpd_por_account_id(obj.account_id, obj.termo_aceite_lgpd)
        if foco:
            obj.data_inclusao_termo_aceite_lgpd = datetime.now()
            obj.save()
        print("(task) Finalizado Integração Pliq ")
    return json.dumps(respostas)
