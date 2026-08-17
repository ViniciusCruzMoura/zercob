from celery import shared_task

@shared_task(name="Atualizar Dias em Atraso doc Contratos", time_limit=600, soft_time_limit=600)
def task_contratos_atualizar_atraso():
    result_data = ""
    return result_data
