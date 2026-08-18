from celery import shared_task

@shared_task(name="Atualizar Dias em Atraso doc Contratos", time_limit=600, soft_time_limit=600)
def task_contratos_atualizar_atraso():
    result_data = ""

    organizacoes = Organizacao.objects.all()
    for organizacao in organizacoes:
        carteiras organizacao.carteiras.all()
        for carteira in carteiras:
            contratos = carteira.contratos.all()
            for contrato in contratos:
                print(">> ", contrato)

    return result_data
