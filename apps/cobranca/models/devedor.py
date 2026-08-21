from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class DevedoresEnderecos(models.Model):
    id = models.BigAutoField(primary_key=True)
    devedor = models.ForeignKey(
        'Devedores',
        on_delete=models.CASCADE,
    )
    cep = models.CharField(
        max_length=300,
        null=True,
        db_index=True,
        help_text="CEP",
        db_comment="CEP",
        verbose_name="CEP",
    )
    logradouro = models.CharField(
        max_length=300,
        null=True,
        help_text="Logradouro",
        db_comment="Logradouro",
        verbose_name="Logradouro",
    )
    bairro = models.CharField(
        max_length=300,
        null=True,
        help_text="Bairro",
        db_comment="Bairro",
        verbose_name="Bairro",
    )
    municipio = models.CharField(
        max_length=300,
        null=True,
        help_text="Municipio",
        db_comment="Municipio",
        verbose_name="Municipio",
    )
    latitude = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Latitude",
        db_comment="Latitude",
        verbose_name="Latitude",
    )
    longitude = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Longitude",
        db_comment="Longitude",
        verbose_name="Longitude",
    )
    UF_CHOICES = {
        1: "Acre",
        2: "Amapá",
        3: "Amazonas",
        4: "Pará",
        5: "Rondônia",
        6: "Roraima",
        7: "Tocantins",
        8: "Alagoas",
        9: "Bahia",
        10: "Ceará",
        11: "Maranhão",
        12: "Paraiba",
        13: "Pernambuco",
        14: "Piauí",
        15: "Rio Grande do Norte",
        16: "Sergipe",
        17: "Distrito Federal",
        18: "Goiás",
        19: "Mato Grosso",
        20: "Mato Grosso do Sul",
        21: "Espírito Santo",
        22: "Minas Gerais",
        23: "Rio de Janeiro",
        24: "São Paulo",
        25: "Paraná",
        26: "Rio Grande do Sul",
        27: "Santa Catarina",
    }
    uf = models.IntegerField(
        help_text="UF",
        db_comment="UF",
        verbose_name="UF",
        choices=UF_CHOICES,
    )
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "devedores_enderecos"
        verbose_name = "Endereço do Devedor"
        verbose_name_plural = "Endereços do Devedor"
        db_table_comment = "Endereços do Devedor"
        permissions = (
            ('import_devedoresenderecos', 'Can import'),
            ('export_devedoresenderecos', 'Can export'),
        )

class DevedoresContatos(models.Model):
    id = models.BigAutoField(primary_key=True)

    devedor = models.ForeignKey(
        'Devedores',
        on_delete=models.CASCADE,
    )

    TELEFONE = 1
    EMAIL = 2
    TIPO_CHOICES = {
        TELEFONE: "Telefone",
        EMAIL: "E-mail",
    }
    tipo = models.IntegerField(
        help_text="Tipo",
        db_comment="Tipo",
        verbose_name="Tipo",
        choices=TIPO_CHOICES,
        default=TELEFONE,
    )
    contato = models.CharField(
        max_length=500,
        help_text="Contato",
        db_comment="Contato",
        verbose_name="Contato",
        validators=[
            RegexValidator(
                regex=r'^\+55\s\d{2}\s\d{4,5}-\d{4}$|^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
                message='Contato Invalido.'
            )
        ],
    )
    observacao = models.TextField(
        max_length=3000,
        help_text="Observação",
        db_comment="Observação",
        verbose_name="Observação",
    )
    HOT = 1
    INVALIDO = 2
    DESCONHECIDO = 3
    VAZIO = 4
    CONFIANCA_CHOICES = {
        HOT: "HOT — contato confirmado (já conseguimos falar com o devedor por ele)",
        INVALIDO: "Inválido — sabidamente errado (número não existe / e-mail retorna erro)",
        DESCONHECIDO: "Desconhecido - atende mas não é o devedor",
        VAZIO: "(vazio) - ainda não testado",
    }
    confianca = models.IntegerField(
        help_text="Confiança",
        db_comment="Confiança",
        verbose_name="Confiança",
        choices=CONFIANCA_CHOICES,
        default=VAZIO,
    )
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "devedores_contatos"
        verbose_name = "Contato do Devedor"
        verbose_name_plural = "Contatos do Devedor"
        db_table_comment = "Contatos do Devedor"
        permissions = (
            ('import_devedorescontatos', 'Can import'),
            ('export_devedorescontatos', 'Can export'),
        )

class Devedores(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome_cliente = models.CharField(
        max_length=500,
        help_text="Nome do Cliente",
        db_comment="Nome do Cliente",
        verbose_name="Nome do Cliente",
    )
    cpf_cnpj = models.CharField(
        max_length=300,
        help_text="CPF ou CNPJ (com ou sem pontuação).",
        db_comment="CPF/CNPJ",
        verbose_name="CPF/CNPJ",
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}|\d{14}', 
                message=(
                    'Informe um CPF (xxx.xxx.xxx-xx ou só dígitos) ou um CNPJ '
                    '(xx.xxx.xxx/xxxx-xx ou só dígitos).'
                )
            ),
        ],
        unique=True,
    )
#     numero_contrato = models.CharField(
#         max_length=300,
#         help_text="Numero do Contrato",
#         db_comment="Numero do Contrato",
#         verbose_name="Numero do Contrato",
#         db_index=True,
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
#     titulo = models.CharField(
#         max_length=300,
#         help_text="Titulo",
#         db_comment="Titulo",
#         verbose_name="Titulo",
#         db_index=True,
#     )

    def __str__(self):
        return f"{self.nome_cliente} ({self.cpf_cnpj})"
    class Meta:
        #abstract = True
        db_table = "devedores"
        verbose_name = "Devedores"
        verbose_name_plural = "Devedores"
        db_table_comment = "Devedores"
        permissions = (
            ('import_devedores', 'Can import'),
            ('export_devedores', 'Can export'),
            ('viewall_devedores', 'Can view all Arquivo do Solfacil Acordo'),
        )
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['student_id', 'course_code'],
#                 name='unique_student_registration'
#             )
#         ]
