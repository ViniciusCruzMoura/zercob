from tablib import Dataset
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, IntegerWidget, DateWidget

from apps.cobranca.models.devedor import (
    Devedores,
    DevedoresEnderecos,
    DevedoresContatos,
)
from apps.cobranca.models.carteira import Carteiras
from apps.cobranca.models.contrato import Contratos, ContratosParcelas


class UFWidget(IntegerWidget):
    UFS = {
        "AC": 1,
        "AP": 2,
        "AM": 3,
        "PA": 4,
        "RO": 5,
        "RR": 6,
        "TO": 7,
        "AL": 8,
        "BA": 9,
        "CE": 10,
        "MA": 11,
        "PB": 12,
        "PE": 13,
        "PI": 14,
        "RN": 15,
        "SE": 16,
        "DF": 17,
        "GO": 18,
        "MT": 19,
        "MS": 20,
        "ES": 21,
        "MG": 22,
        "RJ": 23,
        "SP": 24,
        "PR": 25,
        "RS": 26,
        "SC": 27,
    }

    def clean(self, value, row=None, **kwargs):
        if value in (None, ""):
            return None

        value = str(value).strip().upper()

        if value.isdigit():
            return int(value)

        if value not in self.UFS:
            raise ValueError(f"UF inválida: {value}")

        return self.UFS[value]


class TipoContatoWidget(IntegerWidget):
    def clean(self, value, row=None, **kwargs):
        value = str(value).strip().upper()

        choices = {
            "1": DevedoresContatos.TELEFONE,
            "TELEFONE": DevedoresContatos.TELEFONE,
            "2": DevedoresContatos.EMAIL,
            "EMAIL": DevedoresContatos.EMAIL,
            "E-MAIL": DevedoresContatos.EMAIL,
        }

        if value not in choices:
            raise ValueError(f"Tipo de contato inválido: {value}")

        return choices[value]


class ConfiancaContatoWidget(IntegerWidget):
    def clean(self, value, row=None, **kwargs):
        value = str(value).strip().upper()

        choices = {
            "1": DevedoresContatos.HOT,
            "HOT": DevedoresContatos.HOT,

            "2": DevedoresContatos.INVALIDO,
            "INVALIDO": DevedoresContatos.INVALIDO,
            "INVÁLIDO": DevedoresContatos.INVALIDO,

            "3": DevedoresContatos.DESCONHECIDO,
            "DESCONHECIDO": DevedoresContatos.DESCONHECIDO,

            "4": DevedoresContatos.VAZIO,
            "VAZIO": DevedoresContatos.VAZIO,
        }

        if value not in choices:
            raise ValueError(f"Confiança inválida: {value}")

        return choices[value]


# ============================================================
# LAYOUT 1
# NOME, CPF/CNPJ
# ============================================================

class DevedoresResource(resources.ModelResource):
    nome_cliente = fields.Field(
        column_name="NOME",
        attribute="nome_cliente",
    )

    cpf_cnpj = fields.Field(
        column_name="CPF/CNPJ",
        attribute="cpf_cnpj",
    )

    class Meta:
        model = Devedores
        fields = (
            "nome_cliente",
            "cpf_cnpj",
        )
        import_id_fields = ("cpf_cnpj",)
        skip_unchanged = True
        name = "01 - Devedores"


# ============================================================
# LAYOUT 2
# CPF/CNPJ, CEP, LOGRADOURO, BAIRRO, MUNICIPIO, UF
# ============================================================

class DevedoresEnderecosResource(resources.ModelResource):
    devedor = fields.Field(
        column_name="CPF/CNPJ",
        attribute="devedor",
        widget=ForeignKeyWidget(
            Devedores,
            field="cpf_cnpj",
        ),
    )

    cep = fields.Field(
        column_name="CEP",
        attribute="cep",
    )

    logradouro = fields.Field(
        column_name="LOGRADOURO",
        attribute="logradouro",
    )

    bairro = fields.Field(
        column_name="BAIRRO",
        attribute="bairro",
    )

    municipio = fields.Field(
        column_name="MUNICIPIO",
        attribute="municipio",
    )

    uf = fields.Field(
        column_name="UF",
        attribute="uf",
        widget=UFWidget(),
    )

    class Meta:
        model = DevedoresEnderecos
        fields = (
            "devedor",
            "cep",
            "logradouro",
            "bairro",
            "municipio",
            "uf",
        )
        import_id_fields = (
            "devedor",
            "cep",
            "logradouro",
        )
        skip_unchanged = True
        name = "02 - Endereços"


# ============================================================
# LAYOUT 3
# CPF/CNPJ, TIPO, CONTATO, CONFIANÇA
# ============================================================

class DevedoresContatosResource(resources.ModelResource):
    devedor = fields.Field(
        column_name="CPF/CNPJ",
        attribute="devedor",
        widget=ForeignKeyWidget(
            Devedores,
            field="cpf_cnpj",
        ),
    )

    tipo = fields.Field(
        column_name="TIPO",
        attribute="tipo",
        widget=TipoContatoWidget(),
    )

    contato = fields.Field(
        column_name="CONTATO",
        attribute="contato",
    )

    confianca = fields.Field(
        column_name="CONFIANÇA",
        attribute="confianca",
        widget=ConfiancaContatoWidget(),
    )

    class Meta:
        model = DevedoresContatos
        fields = (
            "devedor",
            "tipo",
            "contato",
            "confianca",
        )
        import_id_fields = (
            "devedor",
            "tipo",
            "contato",
        )
        skip_unchanged = True
        name = "03 - Contatos"


# ============================================================
# LAYOUT 4
# CARTEIRA, CPF/CNPJ, PRODUTO,
# N° PARCELA, DATA VENCIMENTO, VALOR
# ============================================================

class ContratosParcelasResource(resources.ModelResource):
    carteira = fields.Field(
        column_name="CARTEIRA",
        attribute="carteira",
        widget=ForeignKeyWidget(
            Carteiras,
            field="nome",
        ),
    )

    devedor = fields.Field(
        column_name="CPF/CNPJ",
        attribute="devedor",
        widget=ForeignKeyWidget(
            Devedores,
            field="cpf_cnpj",
        ),
    )

    produto = fields.Field(
        column_name="PRODUTO",
        attribute="produto",
    )

    def before_save_instance(self, instance, row, **kwargs):
        if not instance.status:
            instance.status = Contratos.ATIVO

    def after_save_instance(self, instance, row, **kwargs):
        numero_parcela = IntegerWidget().clean(
            row["N° PARCELA"]
        )

        data_vencimento = DateWidget(
            format="%d/%m/%Y"
        ).clean(
            row["DATA VENCIMENTO"]
        )

        valor = IntegerWidget().clean(
            row["VALOR"]
        )

        ContratosParcelas.objects.update_or_create(
            contrato=instance,
            numero_parcela=numero_parcela,
            defaults={
                "data_vencimento": data_vencimento,
                "valor_original": valor,
            },
        )

    class Meta:
        model = Contratos

        fields = (
            "carteira",
            "devedor",
            "produto",
        )

        import_id_fields = (
            "carteira",
            "devedor",
            "produto",
        )

        skip_unchanged = False
        name = "04 - Contratos e Parcelas"



############################
#
# EXPORTADOR
#
############################
class DevedoresCompletoExportResource(resources.ModelResource):

    class Meta:
        model = Devedores
        name = "Devedores Completo"

    def export(self, queryset=None, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.prefetch_related(
            "devedorescontatos_set",
            "devedoresenderecos_set",
        )

        dataset = Dataset(
            headers=[
                "NOME",
                "CPF/CNPJ",
                "TIPO",
                "CONTATO",
                "CONFIANÇA",
                "CEP",
                "LOGRADOURO",
                "BAIRRO",
                "MUNICIPIO",
                "UF",
            ]
        )

        for devedor in queryset:
            contatos = list(devedor.devedorescontatos_set.all())
            enderecos = list(devedor.devedoresenderecos_set.all())

            if not contatos:
                contatos = [None]

            if not enderecos:
                enderecos = [None]

            for contato in contatos:
                for endereco in enderecos:
                    dataset.append([
                        devedor.nome_cliente,
                        devedor.cpf_cnpj,

                        contato.get_tipo_display() if contato else "",
                        contato.contato if contato else "",
                        contato.get_confianca_display() if contato else "",

                        endereco.cep if endereco else "",
                        endereco.logradouro if endereco else "",
                        endereco.bairro if endereco else "",
                        endereco.municipio if endereco else "",
                        endereco.get_uf_display() if endereco else "",
                    ])

        return dataset
