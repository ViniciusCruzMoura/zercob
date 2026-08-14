from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import json

@require_http_methods(["GET"])
def health_check(request):
    from django.db import connections
    from core.settings import DATABASES

    results = []

    # Para cada banco de dados configurado no projeto
    for db_alias in connections:
        try:
            # Executa uma query para verificar a conexão com cada banco de dados
            with connections[db_alias].cursor() as cursor:
                cursor.execute(f"SELECT 1 {'FROM dual' if 'oracle' in DATABASES.get(db_alias)['ENGINE'] else ''}")
            
            # Caso a query tenha sucesso, então é adicionado uma mensagem na lista
            results.append({"database": db_alias, "status": "ok", "message": "Database connection is healthy"})

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("health_check error: ", e)
            # Caso tenha um erro, então é adicionado uma mensagem de erro na lista
            results.append({"database": db_alias, "status": "error", "message": f"Database connection error: {str(e)}"})

    # Verifica o status da conexão de todos dos bancos da dados
    overall_status = "ok" if all(result["status"] == "ok" for result in results) else "error"

    # Caso todas as conexões estão saudaveis, então retorna um json com mensagem de sucesso
    # Caso qualquer conexão tenha problemas, então retorna um json com mensagem de erro
    return HttpResponse(
        json.dumps({"status": overall_status, "results": results}), 
        status=200 if overall_status == "ok" else 500,
        content_type="application/json"
    )
