from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from apps.lgpd.sas import sas_buscar_parceiro_por_codigo, sas_buscar_parceiro_por_cpf
from apps.lgpd.pliq import pliq_cadastrar_contato
from apps.lgpd.salesforce import salesforce_buscar_parceiro_por_cpf
from apps.lgpd.models import SebraeParceiro
from datetime import datetime

@csrf_exempt
@xframe_options_exempt
def dashboard_redirect_to_lgpd(request):
    return redirect(reverse('admin:lgpd_sebraeparceiro_changelist'))

@csrf_exempt
@xframe_options_exempt
def send_message_pliq(request, cgc_cpf):
    # TODO pegar dados do objeto persistido ao inves de buscar no salesforce
    parceiro = salesforce_buscar_parceiro_por_cpf(cgc_cpf)
    if not parceiro or not parceiro.get("records"):
        messages.error(request, "Participante não localizado no FOCO.")
        return redirect(reverse('admin:lgpd_sebraeparceiro_changelist'))

    for c in parceiro.get("records"):
        parceiro = c
        break

    print("Sebrae Parceiro:")
    print("CodSebrae", parceiro.get("CodigoSebrae__c"))
    print("CgcCpf", parceiro.get("ChaveExterna__c"))
    print("CodParceiro", None)
    print("Numero", parceiro.get("NumeroCobranca__c"))
    print("TermoAceiteLGPD", parceiro.get("TermoAceiteLGPD__c"))

    if parceiro.get("TermoAceiteLGPD__c") in ['sim', 'SIM', 'Sim']:
        messages.warning(request, "O participante já Aceitou o Termo de Consentimento LGPD")
        return redirect(reverse('admin:lgpd_sebraeparceiro_changelist'))

    obj = SebraeParceiro.objects.filter(cgc_cpf=cgc_cpf).first()
    if not obj.termo_aceite_lgpd:
        pliq_cadastrar_contato(obj.cgc_cpf, obj.numero, obj.nome_razao_social)
        obj.importacao_contato_pliq = True
        obj.data_inclusao_importacao_pliq = datetime.now()
        obj.qnt_vezes_importado_para_pliq += 1
        obj.save()

#     parceiro = sas_buscar_parceiro_por_cpf(cgc_cpf)
#     if not parceiro:
#         messages.error(request, "Participante não localizado no SAS.")
#         return redirect(reverse('admin:lgpd_sebraeparceiro_changelist'))
#     parceiro = parceiro[0]
# 
#     print("Sebrae Parceiro:")
#     print("CodSebrae", parceiro.get("CodSebrae"))
#     print("CgcCpf", parceiro.get("CgcCpf"))
#     print("CodParceiro", parceiro.get("CodParceiro"))
#     print("Numero", parceiro.get("Numero"))
#     print("TermoAceiteLGPD", parceiro.get("TermoAceiteLGPD"))

#     if parceiro.get("TermoAceiteLGPD") == 1:
#         messages.warning(request, "O participante já Aceitou o Termo LGPD")
#         return redirect(reverse('admin:lgpd_sebraeparceiro_changelist'))
#     pliq = pliq_cadastrar_contato(parceiro.get("CgcCpf"), parceiro.get("Numero"))
#     print(pliq)
#     if not pliq:
#         messages.error(request, "Não foi possivel enviar o Termo LGPD para o Contato.")
#         return redirect(reverse('admin:lgpd_sebraeparceiro_changelist'))

    messages.success(request, 'Mensagem enviada com sucesso. Aguarde alguns minutos para recebimento pelo contato do CPF informado.')

    #messages.info(request, "Three credits remain in your account.")
    #messages.warning(request, "Your account expires in three days.")
    #messages.error(request, "Document deleted.")

    #context = {}
    #return render(request, 'index.html', context)
    #return redirect('admin:index')
    return redirect(reverse('admin:lgpd_sebraeparceiro_changelist'))
