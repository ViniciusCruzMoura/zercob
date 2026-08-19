from django.contrib import admin
from apps.cobranca.models import *
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

# MOD USER
admin.site.unregister(User)
admin.site.unregister(Group)

class UsuarioOrganizacaoInline(StackedInline):
    model = UsuarioOrganizacao
    extra = 1
    max_num = 1
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

class PropostasAdmin(ModelAdmin):
    list_display = ["data_inclusao", "decisao", "usuario_decisao", "observacao"]
    def get_queryset(self, request):
        # `extra_context` contains current changeform object
        obj_id = self.extra_context.get("object")

        # If we are on create object page display no results
        if not obj_id:
            return super().get_queryset(request).none()

        # If there is a permission requirement, make sure that
        # everything is properly handled here
        return super().get_queryset(request).filter(
            contrato__pk=obj_id
        )

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

@admin.register(Acordos)
class AcordosAdmin(ModelAdmin):
    inlines = [AcordosParcelasInline]
#     inlines = [AcordosPagamentosInline, AcordosParcelasInline]
#     list_display = (
#         'devedor__nome_cliente',
#         'devedor__cpf_cnpj',
#     )


# class DevedoresParecelasInline(admin.TabularInline):
#     model = DevedoresParecelas

class DevedoresContatosInline(TabularInline):
    model = DevedoresContatos
    extra = 1
    exclude = ['observacao']
class DevedoresEnderecosInline(TabularInline):
    model = DevedoresEnderecos
    extra = 1
    exclude = ['latitude', 'longitude']
class DevedoresAdmin(ModelAdmin):
    model = Devedores
#     inlines = [DevedoresParecelasInline]
    list_display = (
        'nome_cliente',
        'cpf_cnpj',
    )
    search_fields = ("id", "nome_cliente", "cpf_cnpj")
    inlines = [DevedoresContatosInline, DevedoresEnderecosInline]
    cpf_cnpj_fields = ["cpf_cnpj"]
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        admin_model_get_form_widget(form, self, request, obj, **kwargs)
        return form

# class DevedoresParecelasAdmin(admin.ModelAdmin):
#     model = DevedoresParecelas
# class AcordosParcelasAdmin(admin.ModelAdmin):
#     model = AcordosParcelas
# class AcordosPagamentosAdmin(admin.ModelAdmin):
#     model = AcordosPagamentos

class PropostasDataset(BaseDataset):
    model = Propostas
    model_admin = PropostasAdmin
    #tab = True # Displays this dataset as tab

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
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
#     readonly_fields = ['numero_parcela', 'data_vencimento', 'valor']
@admin.register(Propostas)
class PropostasAdmin(ModelAdmin):
    search_fields = ("id",)
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
    inlines = [PropostasParcelasInline]
    list_display = (
        "contrato",
        "modalidade",
        "qtd_parcelas",
        "status",
    )

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
        'devedor__nome_cliente',
        'devedor__cpf_cnpj',
        'carteira__nome',
        'carteira__nome_responsavel',
    )
    exclude = (
        'ativo',
        'data_inclusao',
        'data_alteracao',
        'usuario_inclusao',
        'usuario_alteracao',
    )
#     list_sections = [
#         ContratosTableSection,
#     ]
#     change_form_datasets = [
#         DevedoresDataset,
#     ]
#     change_form_datasets = [
#         PropostasDataset,
#     ]

class OrganizacaoCarteirasInline(NonrelatedTabularInline):
    model = Carteiras
    extra = 1
    fields = ["id", "nome", "responsavel", "nome_responsavel", "status", "data_inclusao", "ativo"]
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
    extra = 1
    max_num = 1
    tab = 1
    fields = ["a_vista", "parcelas", "juros", "multa", "desconto", "entrada_minima", "maximo_parcelas"]
    percentage_fields = ["juros", "multa", "desconto"]
    currency_fields = ["entrada_minima"]
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
        'nome_responsavel',
        'organizacao__cpf_cnpj',
    )
    #inlines = [ContratosInline]
    inlines = [CarteirasRegrasNegociacaoInline, CarteirasContratosInline]

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
