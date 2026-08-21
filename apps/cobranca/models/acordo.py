from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from apps.cobranca.models.devedor import Devedores

class AcordosParcelas(models.Model):
    id = models.BigAutoField(primary_key=True)

    ativo = models.BooleanField(
        default=True, 
        help_text="Coluna para Exclusão logica do registro",
        db_comment="Coluna para Exclusão logica do registro",
        verbose_name="Registro Ativo",
    )
    data_inclusao = models.DateField(
        blank=True,
        null=True,
        help_text="Data da Inclusão do Processo: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        db_comment="Data da Inclusão do Processo: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data da Inclusão",
        db_index=True,
        auto_now_add=True,
    )
    data_alteracao = models.DateField(
        blank=True,
        null=True,
        help_text="Data da Alteração do Processo: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        db_comment="Data da Alteração do Processo: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data da Alteração",
        db_index=True,
        auto_now_add=True,
    )
    usuario_inclusao = models.CharField(
        max_length=300,
        help_text="Usuario da Inclusão do Processo",
        db_comment="Usuario da Inclusão do Processo",
        verbose_name="Usuario da Inclusão",
        default="sistema",
    )
    usuario_alteracao = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Usuario da Alteração do Processo",
        db_comment="Usuario da Alteração do Processo",
        verbose_name="Usuario da Alteração",
        default="sistema",
    )

    acordo = models.ForeignKey(
        'Acordos',
        on_delete=models.CASCADE,
        related_name='parcelas',
        help_text="Referência à Acordos"
    )

    A_VENCER = 1
    PAGO = 2
    QUEBRA = 3
    STATUS_CHOICES = {
        A_VENCER: "A vencer",
        PAGO: "Pago",
        QUEBRA: "Quebra",
    }
    status = models.IntegerField(
        help_text="Situação",
        db_comment="Situação",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
        default=A_VENCER
    )

    numero_parcela = models.IntegerField(
        db_comment="N° Parcela",
        verbose_name="N° Parcela",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(420),
        ],
    )
    data_vencimento = models.DateField(
        db_comment="Data do Vencimento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data do Vencimento",
        db_index=True,
    )
    valor = models.IntegerField(
        db_comment="Valor da Parcela",
        verbose_name="Valor da Parcela",
        validators=[
            MinValueValidator(0)
        ],
    )

#     parcela_inicio = models.IntegerField(
#         help_text="Parcela Inicial",
#         db_comment="Parcela Inicial",
#         verbose_name="Parcela Inicial",
#         validators=[
#             MinValueValidator(0),
#             MaxValueValidator(120),
#         ],
#         null=True,
#         blank=True,
#     )
#     parcela_final = models.IntegerField(
#         help_text="Parcela Final",
#         db_comment="Parcela Final",
#         verbose_name="Parcela Final",
#         validators=[
#             MinValueValidator(0),
#             MaxValueValidator(120),
#         ],
#         null=True,
#         blank=True,
#     )
#     valor_apagar = models.IntegerField(
#         help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
#         db_comment="Valor A pagar",
#         verbose_name="Valor A pagar",
#         validators=[
#             MinValueValidator(100)
#         ],
#         null=True,
#         blank=True,
#     )
#     valor_pago = models.IntegerField(
#         help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
#         db_comment="Valor Pago",
#         verbose_name="Valor Pago",
#         validators=[
#             MinValueValidator(100)
#         ],
#         null=True,
#         blank=True,
#     )
#     saldo = models.IntegerField(
#         help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
#         db_comment="Valor do Saldo",
#         verbose_name="Valor do Saldo",
#         validators=[
#             MinValueValidator(100)
#         ],
#         null=True,
#         blank=True,
#     )
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "acordos_parcelas"
        verbose_name = "Parcela do Acordo"
        verbose_name_plural = "Parcelas do Acordo"
        db_table_comment = "Parcelas do Acordo"
        permissions = (
            ('import_devedoresparcelas', 'Can import'),
            ('export_devedoresoarcelas', 'Can export')
        )

class Acordos(models.Model):
    id = models.BigAutoField(primary_key=True)
    devedor = models.ForeignKey(
        Devedores, 
        on_delete=models.PROTECT, 
#         blank=True,
#         null=True,
        help_text="Devedor",
        db_comment="Devedor",
        verbose_name="Devedor",
    )

#     contrato = models.ForeignKey(
#         'Contratos',
#         on_delete=models.CASCADE,
#     )
    
#     cpf_cnpj = models.CharField(
#         max_length=300,
#         help_text="CPF ou CNPJ (com ou sem pontuação).",
#         db_comment="CPF/CNPJ",
#         verbose_name="CPF/CNPJ",
#         db_index=True,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}|\d{14}', 
#                 message=(
#                     'Informe um CPF (xxx.xxx.xxx-xx ou só dígitos) ou um CNPJ '
#                     '(xx.xxx.xxx/xxxx-xx ou só dígitos).'
#                 )
#             ),
#         ],
#     )

    A_VISTA = 1
    PARCELADO = 2
    MODALIDADE_CHOICES = {
        A_VISTA: "A vista",
        PARCELADO: "Parcelado",
    }
    modalidade = models.IntegerField(
        help_text="Modalidade",
        db_comment="Modalidade",
        verbose_name="Modalidade",
        choices=MODALIDADE_CHOICES,
        default=A_VISTA,
    )
    valor = models.IntegerField(
        db_comment="Valor",
        verbose_name="Valor",
        validators=[
            MinValueValidator(0)
        ],
    )
    data_vencimento = models.DateField(
        db_comment="Data do Vencimento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data do Vencimento",
        db_index=True,
    )
    AGUARDANDO_PAGAMENTO = 1
    PAGO = 2
    QUEBRADO = 3
    STATUS_CHOICES = {
        AGUARDANDO_PAGAMENTO: "Aguardando Pagamento",
        PAGO: "Pago",
        QUEBRADO: "Quebrado",
    }
    status = models.IntegerField(
        help_text="Situação",
        db_comment="",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
        default=AGUARDANDO_PAGAMENTO
    )

    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "acordos"
        verbose_name = "Acordos"
        verbose_name_plural = "Acordos"
        db_table_comment = "Acordos"
        permissions = (
            ('import_acordos', 'Can import'),
            ('export_acordos', 'Can export'),
            ('viewall_acordos', 'Can view all Arquivo do Solfacil Acordo'),
        )
