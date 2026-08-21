from django.contrib import admin
from datetime import datetime
from apps.cobranca.models.organizacao import *
from apps.cobranca.models.acordo import *
from apps.cobranca.models.devedor import *
from apps.cobranca.models.carteira import *
from apps.cobranca.models.proposta import *
from apps.cobranca.models.contrato import *
from import_export.admin import ImportExportModelAdmin

from unfold.admin import ModelAdmin
from unfold.datasets import BaseDataset
from unfold.admin import StackedInline, TabularInline
from unfold.contrib.inlines.admin import NonrelatedTabularInline
from unfold.sections import TableSection, TemplateSection
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from apps.common.admin_model import admin_model_get_form_widget
from apps.common.guias import guias_formatar_valor

from django.urls import path, reverse
from django.http import JsonResponse

from apps.cobranca.resources.devedor import (
    DevedoresResource,
    DevedoresEnderecosResource,
    DevedoresContatosResource,
    ContratosParcelasResource,
)
from apps.cobranca.resources.devedor import DevedoresCompletoExportResource

# IMPORADORES LAYOUT
# NOME,CPF/CNPJ;
# CPF/CNPJ,CEP,LOGRADOURO,BAIRRO,MUNICIPIO,UF;
# CPF/CNPJ,TIPO,CONTATO,CONFIANÇA;
# CARTEIRA,CPF/CNPJ,PRODUTO,N° PARCELA,DATA VENCIMENTO, VALOR;

# MOD USER
admin.site.unregister(User)
admin.site.unregister(Group)

class UsuarioOrganizacaoInline(StackedInline):
    model = UsuarioOrganizacao
    extra = 1
    max_num = 1
    autocomplete_fields = ['organizacao']
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    inlines = [UsuarioOrganizacaoInline]

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

#admin.site.register(User, UserAdmin)




class ContratosTableSection(TableSection):
#     verbose_name = _("Table title")  # Displays custom table title
#     height = 300  # Force the table height. Ideal for large amount of records
    related_name = "carteira"  # Related model field name
#     fields = ["pk", "title", "custom_field"]  # Fields from related model

    # Custom field
#     def custom_field(self, instance):
#         return instance.pk

# class PropostasAdmin(ModelAdmin):
#     list_display = ["data_inclusao", "decisao", "usuario_decisao", "observacao"]
#     def get_queryset(self, request):
#         # `extra_context` contains current changeform object
#         obj_id = self.extra_context.get("object")
# 
#         # If we are on create object page display no results
#         if not obj_id:
#             return super().get_queryset(request).none()
# 
#         # If there is a permission requirement, make sure that
#         # everything is properly handled here
#         return super().get_queryset(request).filter(
#             contrato__pk=obj_id
#         )

# class AcordosPagamentosInline(admin.TabularInline):
#     model = AcordosPagamentos
#     extra = 1
class AcordosParcelasInline(TabularInline):
    model = AcordosParcelas
    extra = 0
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
    currency_fields = ["valor"]
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        admin_model_get_form_widget(formset.form, self, request, obj, **kwargs)
        return formset

@admin.register(Acordos)
class AcordosAdmin(ImportExportModelAdmin, ModelAdmin):
    inlines = [AcordosParcelasInline]
    search_fields = (
        "id", 
        "devedor__nome_cliente",
        "devedor__cpf_cnpj",
    )
    list_display = (
        "id",
        "devedor__nome_cliente",
        "devedor__cpf_cnpj",
        "status",
#         "numero_parcela",
        "data_vencimento",
        "display_valor",
        "modalidade",
    )
    currency_fields = ["valor"]
#     inlines = [AcordosPagamentosInline, AcordosParcelasInline]
#     list_display = (
#         'devedor__nome_cliente',
#         'devedor__cpf_cnpj',
#     )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        admin_model_get_form_widget(form, self, request, obj, **kwargs)
        return form
    @admin.display(description="Valor",ordering="")
    def display_valor(self, obj):
        return guias_formatar_valor(obj.valor)


# class DevedoresParecelasInline(admin.TabularInline):
#     model = DevedoresParecelas


# class DevedoresParecelasAdmin(admin.ModelAdmin):
#     model = DevedoresParecelas
# class AcordosParcelasAdmin(admin.ModelAdmin):
#     model = AcordosParcelas
# class AcordosPagamentosAdmin(admin.ModelAdmin):
#     model = AcordosPagamentos

# class PropostasDataset(BaseDataset):
#     model = Propostas
#     model_admin = PropostasAdmin
#     #tab = True # Displays this dataset as tab

# class DevedoresDataset(BaseDataset):
#     model = Devedores
#     model_admin = DevedoresAdmin
class CarteirasNonrelatedInline(NonrelatedTabularInline):  # NonrelatedStackedInline is available as well
    model = Carteiras
#     fields = ["nome_cliente", "cpf_cnpj"]  # Ignore property to display all fields
    extra = 0
    max_num = 1
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )

     # 1. Prevent adding new rows
    def has_add_permission(self, request, obj=None):
        return False

    # 2. Prevent deleting existing rows
    def has_delete_permission(self, request, obj=None):
        return False

    # 3. Dynamically make all fields read-only
#     def get_readonly_fields(self, request, obj=None):
#         return [f.name for f in self.model._meta.fields]
    def get_readonly_fields(self, request, obj=None):
        excluded_fields = set(self.exclude or ())
        return [
            field.name
            for field in self.model._meta.fields
            if field.name not in excluded_fields
        ]

    def get_form_queryset(self, obj):
        """
        Gets all nonrelated objects needed for inlines. Method must be implemented.
        """
        if obj and obj.carteira_id:
            return self.model.objects.filter(id=obj.carteira_id)
        return self.model.objects.all()

    def save_new_instance(self, parent, instance):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        pass
class DevedoresNonrelatedInline(NonrelatedTabularInline):  # NonrelatedStackedInline is available as well
    model = Devedores
#     fields = ["nome_cliente", "cpf_cnpj"]  # Ignore property to display all fields
    extra = 0
    max_num = 1
    per_page = 5

     # 1. Prevent adding new rows
    def has_add_permission(self, request, obj=None):
        return False

    # 2. Prevent deleting existing rows
    def has_delete_permission(self, request, obj=None):
        return False

    # 3. Dynamically make all fields read-only
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def get_form_queryset(self, obj):
        """
        Gets all nonrelated objects needed for inlines. Method must be implemented.
        """
        if obj and obj.devedor_id:
            return self.model.objects.filter(id=obj.devedor_id)
        return self.model.objects.all()

    def save_new_instance(self, parent, instance):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        pass

class PropostasParcelasInline(TabularInline):
    model = PropostasParcelas
    extra = 0
    #min_num = 1
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
#     readonly_fields = ['numero_parcela', 'data_vencimento', 'valor']
    currency_fields = ["valor"]
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        admin_model_get_form_widget(formset.form, self, request, obj, **kwargs)
        return formset
class PropostaContratoInline(TabularInline):
    model = PropostaContrato
    extra = 0
    min_num = 1
    # TODO 202608201220 o contrato tem que pertencer ao devedor 
    # TODO 202608201220 filtrar para mostrar apenas contratos do devedor
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        devedor_id = (
            getattr(obj, "devedor_id", None)
            or request.POST.get("devedor")
            or request.GET.get("devedor")
        )

        if "contrato" in formset.form.base_fields:
            if devedor_id:
                formset.form.base_fields["contrato"].queryset = (
                    Contratos.objects.filter(devedor_id=devedor_id)
                )
            else:
                formset.form.base_fields["contrato"].queryset = (
                    Contratos.objects.none()
                )

        return formset
@admin.register(Propostas)
class PropostasAdmin(ModelAdmin):
    class Media:
        js = (
            "admin/js/propostas_contratos.js",
        )
    search_fields = ("id",)
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
    inlines = [PropostaContratoInline, PropostasParcelasInline]
    list_display = (
        "devedor__nome_cliente",
        "devedor__cpf_cnpj",
        "modalidade",
        "qtd_parcelas",
        "status",
    )
    percentage_fields = ["entrada"]
    conditional_fields = {
        "entrada": f"modalidade == {Propostas.PARCELADO}",
        "qtd_parcelas": f"modalidade == {Propostas.PARCELADO}",
    }
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "contratos-por-devedor/",
                self.admin_site.admin_view(self.contratos_por_devedor),
                name="cobranca_propostas_contratos_por_devedor",
            ),
        ]
        return custom_urls + urls
    def contratos_por_devedor(self, request):
        devedor_id = request.GET.get("devedor_id")
        if not devedor_id:
            return JsonResponse({"results": []})
        contratos = Contratos.objects.filter(
            devedor_id=devedor_id
        )
        return JsonResponse({
            "results": [
                {
                    "id": contrato.id,
                    "text": str(contrato),
                }
                for contrato in contratos
            ]
        })
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        admin_model_get_form_widget(form, self, request, obj, **kwargs)
        # para adicionar o filtro dinamico no campo de contratos 
        form.base_fields["devedor"].widget.attrs[
            "data-contratos-url"
        ] = reverse(
            "admin:cobranca_propostas_contratos_por_devedor"
        )
        return form

class ContratosParcelasInline(TabularInline):
    model = ContratosParcelas
    extra = 0
    exclude = ('ativo', 'data_inclusao', 'data_alteracao', 'usuario_inclusao', 'usuario_alteracao', 'valor_atualizado')
    readonly_fields = ['display_valor_atualizado', 'status', 'atraso']
    currency_fields = ["valor_original"]
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        admin_model_get_form_widget(formset.form, self, request, obj, **kwargs)
        return formset
    @admin.display(description="Valor (Juros + Multa)",ordering="valor_atualizado")
    def display_valor_atualizado(self, obj):
        return obj.display_valor_atualizado()
# class PropostasInline(TabularInline):
#     model = Propostas
#     extra = 0
#     per_page = 5
#     exclude = ('ativo', 'data_inclusao', 'data_alteracao', 'usuario_inclusao', 'usuario_alteracao')
@admin.register(Contratos)
class ContratosAdmin(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    search_fields = ("id",)  # add real searchable fields, e.g. "numero"
    autocomplete_fields = ("carteira", "devedor",)  # FK field on Contratos that points to Carteiras
    inlines = [ContratosParcelasInline]#[CarteirasNonrelatedInline, DevedoresNonrelatedInline, ContratosParcelasInline]#, PropostasInline]
    list_display = (
        'id',
        'display_nome_devedor',
        'display_cpf_cnpj_devedor',
        'display_nome_carteira',
        'display_qtd_parcelas_vencidas',
        'display_maior_atraso',
        'display_valor_total_parcelas_vencidas',
    )
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
    # TODO 202608201027 colocar isso dentro do model para poder
    # reutilizar
    @admin.display(description="Devedor",ordering="devedor__nome_cliente")
    def display_nome_devedor(self, obj):
        return obj.devedor.nome_cliente
    @admin.display(description="CPF/CNPJ",ordering="devedor__cpf_cnpj")
    def display_cpf_cnpj_devedor(self, obj):
        return obj.devedor.cpf_cnpj
    @admin.display(description="Carteira",ordering="carteira__nome")
    def display_nome_carteira(self, obj):
        return obj.carteira.nome
    @admin.display(description="Parcelas (vencidos)",ordering="")
    def display_qtd_parcelas_vencidas(self, obj):
        # vw_parcelas_vencidas_por_contrato(contrato_id)
        return f"{ContratosParcelas.objects.filter(contrato_id=obj.id, data_vencimento__lt=datetime.now().date()).count()}"
    @admin.display(description="Atraso (dias)",ordering="")
    def display_maior_atraso(self, obj):
        # vw_maior_atraso_por_contrato(contrato_id)
        maior_atraso = 0
        parcelas = ContratosParcelas.objects.filter(contrato_id=obj.id, data_vencimento__lt=datetime.now().date())
        for parcela in parcelas:
            if parcela.atraso > maior_atraso:
                maior_atraso = parcela.atraso
        return f"{maior_atraso}"
    @admin.display(description="Débito (vencidos)",ordering="")
    def display_valor_total_parcelas_vencidas(self, obj):
        valor_total = 0
        parcelas = ContratosParcelas.objects.filter(contrato_id=obj.id, data_vencimento__lt=datetime.now().date())
        for parcela in parcelas:
            valor_total += parcela.valor_atualizado
        return guias_formatar_valor(valor_total)
    #display_valor_total_parcelas_vencidas.short_description = "Debito"
    #display_valor_total_parcelas_vencidas.admin_order_field = "debito"
#     list_sections = [
#         ContratosTableSection,
#     ]
#     change_form_datasets = [
#         DevedoresDataset,
#     ]
#     change_form_datasets = [
#         PropostasDataset,
#     ]
    def get_queryset(self, request):
        # isso é para funcionar o relacionamento de dataset
        if getattr(self, "extra_context", None) and self.extra_context:
            devedor_id = self.extra_context.get("object")
            if not devedor_id:
                return super().get_queryset(request).none()
            return super().get_queryset(request).filter(devedor_id=devedor_id)
        return super().get_queryset(request)
class DevedoresContratosDataset(BaseDataset):
    model_admin = ContratosAdmin
    model = Contratos
    tab = True
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         
#         # Filter data based on user or conditions
#         if not request.user.is_superuser:
#             qs = qs.filter(user=request.user)
#             
#         # Optimize performance
#         return qs.select_related("category").order_by("-created_at")
class DevedoresContatosInline(TabularInline):
    model = DevedoresContatos
    extra = 1
    exclude = ['observacao']
class DevedoresEnderecosInline(TabularInline):
    model = DevedoresEnderecos
    extra = 1
    exclude = ['latitude', 'longitude']
class DevedoresAdmin(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    def get_import_resource_classes(self, request):
        return [
            DevedoresResource,
            DevedoresEnderecosResource,
            DevedoresContatosResource,
            ContratosParcelasResource,
        ]
    def get_export_resource_classes(self, request):
        return [
            DevedoresCompletoExportResource,
        ]
    model = Devedores
#     inlines = [DevedoresParecelasInline]
    list_display = (
        'nome_cliente',
        'cpf_cnpj',
        "display_qtd_parcelas_vencidas",
        "display_maior_atraso",
        "display_valor_total_parcelas_vencidas",
        "display_qtd_contratos",
    )
    search_fields = ("id", "nome_cliente", "cpf_cnpj")
    inlines = [DevedoresContatosInline, DevedoresEnderecosInline]
    change_form_datasets = [
        DevedoresContratosDataset,
    ]
    cpf_cnpj_fields = ["cpf_cnpj"]
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        admin_model_get_form_widget(form, self, request, obj, **kwargs)
        return form
    @admin.display(description="Parcelas (vencidos)",ordering="")
    def display_qtd_parcelas_vencidas(self, obj):
        qtd_parcelas_vencidas = 0
        contratos = Contratos.objects.filter(devedor_id=obj.id)
        for contrato in contratos:
            parcelas = ContratosParcelas.objects.filter(
                contrato_id=contrato.id,
                data_vencimento__lt=datetime.now().date()
            )
            qtd_parcelas_vencidas += parcelas.count()
        return qtd_parcelas_vencidas
    @admin.display(description="Atraso (dias)",ordering="")
    def display_maior_atraso(self, obj):
        # TODO 202608201233 proc_calc_maior_atraso_multicontratos(in_devedor_id)
        # TODO 202608201234 vw_get_contratos_vencidos_by_devedor(in_devedor_id)
        maior_atraso = 0
        contratos = Contratos.objects.filter(devedor_id=obj.id)
        for contrato in contratos:
            parcelas = ContratosParcelas.objects.filter(
                contrato_id=contrato.id,
                data_vencimento__lt=datetime.now().date()
            )
            for parcela in parcelas:
                if parcela.atraso > maior_atraso:
                    maior_atraso = parcela.atraso
        return maior_atraso
    @admin.display(description="Débito (vencidos)",ordering="")
    def display_valor_total_parcelas_vencidas(self, obj):
        valor_total = 0
        contratos = Contratos.objects.filter(devedor_id=obj.id)
        for contrato in contratos:
            parcelas = ContratosParcelas.objects.filter(
                contrato_id=contrato.id,
                data_vencimento__lt=datetime.now().date()
            )
            for parcela in parcelas:
                valor_total += parcela.valor_atualizado
        return guias_formatar_valor(valor_total)
    @admin.display(description="Contratos (com debito)",ordering="")
    def display_qtd_contratos(self, obj):
        return Contratos.objects.filter(devedor_id=obj.id).count()

class OrganizacaoCarteirasInline(NonrelatedTabularInline):
    model = Carteiras
    extra = 1
    fields = ["id", "nome", "status", "data_inclusao", "ativo"]
    per_page = 5
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
    def get_form_queryset(self, obj):
        if obj and obj.id:
            return self.model.objects.filter(organizacao_id=obj.id)
        return self.model.objects.all()
    def save_new_instance(self, parent, instance):
        pass
class OrganizacaoRegrasCobrancaInline(TabularInline):
    model = OrganizacaoRegrasCobranca
    extra = 0
    #exclude = ["data_alteracao", "usuario_inclusao", "usuario_alteracao"]
    #readonly_fields = ["ativo", "data_inclusao", "data_alteracao", "usuario_inclusao", "usuario_alteracao"]
#     def get_formset(self, request, obj=None, **kwargs):
#         formset = super().get_formset(request, obj, **kwargs)
# 
#         original_init = formset.form.__init__
# 
#         def custom_init(form, *args, **form_kwargs):
#             original_init(form, *args, **form_kwargs)
# 
#             field = form.fields["atraso"]
# 
#             # Server-side validation
#             field.min_value = -10
#             field.max_value = 10
# 
#             # Browser-side limits, keeping the default widget
#             field.widget.attrs.update({
#                 "min": -10,
#                 "max": 10,
#                 "step": 1,
#             })
# 
#         formset.form.__init__ = custom_init
# 
#         return formset

class UsuarioOrganizacao2Inline(NonrelatedTabularInline):
    model = User
    extra = 1
    fields = ["id", "username", "first_name", "last_name", "email", "is_active"]
    per_page = 5
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
    def get_form_queryset(self, obj):
        if obj and obj.id:
            return self.model.objects.filter(usuarioorganizacao__organizacao=obj)
            #return self.model.objects.filter(organizacao_id=obj.id)
        return self.model.objects.all()
    def save_new_instance(self, parent, instance):
        pass
@admin.register(Organizacao)
class OrganizacaoAdmin(ModelAdmin):
    search_fields = ("id", "cpf_cnpj", "razao_social", "nome_fantasia")
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
    list_display = ["cpf_cnpj", "razao_social", "nome_fantasia", "telefone", "email_institucional"]
    inlines = [OrganizacaoRegrasCobrancaInline, OrganizacaoCarteirasInline, UsuarioOrganizacao2Inline]
    cpf_cnpj_fields = ["cpf_cnpj"]
    phone_fields = ["telefone"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        admin_model_get_form_widget(form, self, request, obj, **kwargs)
        return form

class CarteirasContratosInline(NonrelatedTabularInline):
    model = Contratos
    extra = 0
    per_page = 5
    tab = 1
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        excluded_fields = set(self.exclude or ())
        return [
            field.name
            for field in self.model._meta.fields
            if field.name not in excluded_fields
        ]
    def get_form_queryset(self, obj):
        if obj and obj.id:
            return self.model.objects.filter(carteira_id=obj.id)
        return self.model.objects.all()
    def save_new_instance(self, parent, instance):
        pass

class CarteirasRegrasNegociacaoInline(StackedInline):
    model = CarteirasRegrasNegociacao
    extra = 0
    min_num = 1
    max_num = 1
    fields = ["a_vista", "parcelas", "juros", "multa", "desconto", "entrada_minima", "maximo_parcelas"]
    percentage_fields = ["juros", "multa", "desconto", "entrada_minima"]
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
#         original_init = formset.form.__init__
#         def custom_init(form, *args, **form_kwargs):
#             original_init(form, *args, **form_kwargs)
# 
#             field = form.fields["juros"]
# 
#             # Server-side validation
#             field.min_value = 0
#             field.max_value = 100
# 
#             # Browser-side limits, keeping the default widget
#             field.widget.attrs.update({
#                 "min": 0,
#                 "max": 100,
#                 "step": 1,
#             })
#         formset.form.__init__ = custom_init

        admin_model_get_form_widget(formset.form, self, request, obj, **kwargs)

        return formset
class ContratosInline(admin.TabularInline):
    model = Contratos
    extra = 1
@admin.register(Carteiras)
class CarteirasAdmin(ModelAdmin):
    autocomplete_fields = ['organizacao']
    search_fields = ("id", "nome", "nome_empresa_responsavel")  # add real searchable fields, e.g. "numero"
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
    list_display = (
        'nome',
        'organizacao__cpf_cnpj',
        'status',
        'display_qtd_contratos',
        'display_qtd_devedores',
    )
    #inlines = [ContratosInline]
    inlines = [CarteirasRegrasNegociacaoInline, CarteirasContratosInline]
    @admin.display(description="Quantidade de Devedores", ordering="")
    def display_qtd_devedores(self, obj):
        devedores_ids = set()
        for obj in Contratos.objects.filter(carteira_id=obj.id):
            devedores_ids.add(obj.devedor_id)
        return Devedores.objects.filter(id__in=devedores_ids).count()
    @admin.display(description="Quantidade de Contratos", ordering="")
    def display_qtd_contratos(self, obj):
        return Contratos.objects.filter(carteira_id=obj.id).count()

# class ContratosInline(admin.TabularInline):
#     model = Contratos
#     extra = 1
# class CarteirasAdmin(admin.ModelAdmin):
# #     inlines = [ContratosInline]
#     pass
# 
# class PropostasInline(admin.TabularInline):
#     model = Propostas
#     extra = 1
# class ContratosAdmin(admin.ModelAdmin):
#     autocomplete_fields = ("carteira",)
#     search_fields = ("id",)
#     inlines = [PropostasInline]
# 
# # class ContratosInline(admin.TabularInline):
# #     model = Contratos
# class PropostasAdmin(admin.ModelAdmin):
# #     inlines = [ContratosInline]
#     pass



# admin.site.register(DevedoresParecelas, DevedoresParecelasAdmin)
admin.site.register(Devedores, DevedoresAdmin)
# admin.site.register(AcordosParcelas, AcordosParcelasAdmin)
# admin.site.register(AcordosPagamentos, AcordosPagamentosAdmin)
# admin.site.register(Acordos, AcordosAdmin)
# admin.site.register(Carteiras, CarteirasAdmin)
# admin.site.register(Contratos, ContratosAdmin)
# admin.site.register(Propostas, PropostasAdmin)










# ============================================================
# https://unfoldadmin.com/docs/integrations/django-celery-beat/
# ============================================================
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

from django_celery_beat.models import (
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
)
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget

admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm

@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass
