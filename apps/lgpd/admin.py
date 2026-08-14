from django.contrib import admin
from apps.lgpd.models import SebraeParceiro
from django.utils.html import format_html

# @admin.register(SebraeParceiro)
class SebraeParceiroAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'cgc_cpf',
        'numero',
        'nome_razao_social',
        'importacao_contato_pliq',
        'termo_aceite_lgpd',
        'btn_detalhamento',
    )
    search_fields = (
        'desc_sebrae',
        'nome_razao_social',
        'numero',
    )
    list_filter = (
        'situacao',
        'deficiencia',
        'data_inclusao',
    )
    ordering = ('cod_sebrae',)
    date_hierarchy = 'data_inclusao'

    fieldsets = (
        (None, {
            'fields': ('cgc_cpf', 'nome_razao_social', 'numero', 'desc_sebrae')
        }),
#         ('Endereço', {
#             'fields': ('cod_cid', 'desc_cid', 'cod_est', 'desc_est'),
#             'classes': ('navtab',)  # Seção colapsável
#         }),
#         ('Situação', {
#             'fields': ('situacao', 'deficiencia', 'sit_cadastral', 'desc_sit_cadastral'),
#             'classes': ('navtab',)  # Seção colapsável
#         }),
        ('Datas', {
            'fields': ('data_inclusao', 'data_ultima_alteracao'),
            'classes': ('navtab',)  # Seção colapsável
        }),
        ('Termo de Aceite LGPD', {
            'fields': ('termo_aceite_lgpd', 'data_inclusao_termo_aceite_lgpd'),
            'classes': ('navtab',)  # Seção colapsável
        }),
        ('PliQ', {
            'fields': ('importacao_contato_pliq', 'data_inclusao_importacao_pliq', 'qnt_vezes_importado_para_pliq'),
            'classes': ('navtab',)  # Seção colapsável
        }),
    )
    readonly_fields = [
            'cod_sebrae', 'desc_sebrae', 'cod_parceiro', 'numero', 
            'nome_razao_social', 'cod_cid', 'desc_cid', 'cod_est', 'desc_est', 
            'situacao', 'deficiencia', 'sit_cadastral', 'desc_sit_cadastral',
            'data_inclusao', 'data_ultima_alteracao', 'termo_aceite_lgpd', 'data_inclusao_termo_aceite_lgpd',
            'cod_sebrae_termo_aceite_lgpd', 'desc_sebrae_termo_aceite_lgpd', 'cod_parceiro_termo_aceite_lgpd', 'nome_parceiro_termo_aceite_lgpd',
            'importacao_contato_pliq', 'data_inclusao_importacao_pliq', 'qnt_vezes_importado_para_pliq',
            ]

    @admin.display(description="", ordering="")
    def btn_detalhamento(self, obj):
        html = f"""
        <div class="btn-group float-right">
            <a href="/lgpd/sebraeparceiro/{obj.cgc_cpf}/pliq/send?q={obj.cod_parceiro}" class="btn btn-xs btn-info changelink">Reenviar</a>
            <a href="/lgpd/sebraeparceiro/{obj.cgc_cpf}/change/" class="btn btn-xs btn-primary changelink">Detalhe</a>
        </div>
        """
        return format_html(html)

#     def save_model(self, request, obj, form, change):
#         from django.contrib import messages
#         from apps.lgpd.views import buscar_parceiro_por_cpf
#         parceiro = buscar_parceiro_por_cpf(obj.cgc_cpf)
#         if not parceiro:
#             return self.message_user(request, "Participante não localizado no SAS.", level=messages.ERROR)
#         else:
#             super().save_model(request, obj, form, change)
# 
#     def response_add(self, request, *args, **kwargs):
#         #from django.contrib import messages
#         #self.message_user(request, "Participante localizado e salvo com sucesso.", level=messages.SUCCESS)
#         from django.contrib import messages
#         from apps.lgpd.views import buscar_parceiro_por_cpf
#         parceiro = buscar_parceiro_por_cpf(obj.cgc_cpf)
#         if not parceiro:
#             return self.message_user(request, "Participante não localizado no SAS.", level=messages.ERROR)
#         return super().response_add(request, *args, **kwargs)
# 
#     def response_change(self, request, *args, **kwargs):
#         from django.contrib import messages
#         from apps.lgpd.views import buscar_parceiro_por_cpf
#         parceiro = buscar_parceiro_por_cpf(obj.cgc_cpf)
#         if not parceiro:
#             return self.message_user(request, "Participante não localizado no SAS.", level=messages.ERROR)
#         return super().response_change(request, *args, **kwargs)

