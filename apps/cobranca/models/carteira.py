from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class CarteirasRegrasNegociacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    carteira = models.ForeignKey(
        'Carteiras',
        on_delete=models.CASCADE,
    )
    juros = models.IntegerField(
        help_text="% de Juros",
        db_comment="% Juros",
        verbose_name="% Juros",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        default=0,
    )
    multa = models.IntegerField(
        help_text="% de Multa",
        db_comment="% Multa",
        verbose_name="% Multa",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        default=0,
    )
    a_vista = models.BooleanField(
        default=True, 
        help_text="Permitir Pagamentos A Vista",
        db_comment="Permitir Pagamentos A Vista",
        verbose_name="Pagamentos A Vista",
    )
    parcelas = models.BooleanField(
        default=True, 
        help_text="Permitir Pagamentos Parcelado",
        db_comment="Permitir Pagamentos Parcelado",
        verbose_name="Pagamentos Parcelado",
    )
    desconto = models.IntegerField(
        help_text="% de Desconto",
        db_comment="% Desconto",
        verbose_name="% Desconto (A Vista)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        default=0,
    )
    entrada_minima = models.IntegerField(
        help_text="% Entrada Minima (parcelado)",
        db_comment="% Entrada Minima (parcelado)",
        verbose_name="% Entrada Minima (parcelado)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        default=0,
    )
    maximo_parcelas = models.IntegerField(
        help_text="Quantidade Maxima de Parcelas",
        db_comment="Quantidade Maxima de Parcelas",
        verbose_name="Quantidade Maxima de Parcelas",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(420),
        ],
        default=1,
    )

    def trg_biu_modalidade_defaults(self):
        if not self.parcelas:
            self.entrada_minima = 0
            self.maximo_parcelas = 0
        if not self.a_vista:
            self.desconto = 0
    def clean(self):
        super().clean()
    def save(self, *args, **kwargs):
        # TODO 202608202223 caso seja apenas parcela
        # setar desconto como 0
        # caso seja apenas a vista setar qtd max parcelas
        # e entrada min como 0
        self.trg_biu_modalidade_defaults()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "carteiras_regras_negociacao"
        verbose_name = "Regra de Negociação"
        verbose_name_plural = "Regras de Neogiciação"
        db_table_comment = "Regras de Neogiciação"
        permissions = (
            ('import_carteirasregrasnegociacao', 'Can import'),
            ('export_carteirasregrasnegociacao', 'Can export')
        )

class Carteiras(models.Model):
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

#     UPLOAD = 1
#     API = 2
#     FTP = 3
#     DIGITACAO = 4
#     INTEGRACAO = 5
#     ORIGEM_CHOICES = {
#         UPLOAD: "Upload",
#         API: "API",
#         FTP: "FTP",
#         DIGITACAO: "Digitação",
#         INTEGRACAO: "Integração",
#     }
#     origem = models.IntegerField(
#         help_text="Origem da Carga",
#         db_comment="",
#         verbose_name="Origem da Carga",
#         choices=ORIGEM_CHOICES,
#         default=EM_CADASTRO
#     )

    organizacao = models.ForeignKey(
        'Organizacao',
        on_delete=models.PROTECT,
    )

    EM_CADASTRO = 1
    EM_VALIDACAO = 2
    DISPONIVEL_PARA_OPERACAO = 3
    BLOQUEADA = 4
    CANCELADA = 5
    STATUS_CHOICES = {
        EM_CADASTRO: "Em cadastro",
        EM_VALIDACAO: "Em validação",
        DISPONIVEL_PARA_OPERACAO: "Disponivel para Operação",
        BLOQUEADA: "Bloqueda",
        CANCELADA: "Cancelada",
    }
    status = models.IntegerField(
        help_text="Situação",
        db_comment="",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
        default=EM_CADASTRO
    )
    nome = models.CharField(
        max_length=150,
        help_text="Nome",
        db_comment="Nome",
        verbose_name="Nome",
    )
#     observacao = models.TextField(
#         max_length=3000,
#         help_text="Observação",
#         db_comment="Observação",
#         verbose_name="Observação",
#     )

#     responsavel = models.ForeignKey(
#         User,
#         on_delete=models.PROTECT,
#         blank=True,
#         null=True,
#         help_text="Responsavel pela Carteira",
#         db_comment="Responsavel pela Carteira",
#         verbose_name="Responsavel pela Carteira",
#     )
#     ZEROU = 1
#     CLIENTE_PROPRIETARIO = 2
#     PARCEIRO = 3
#     TIPO_RESPONSAVEL_CHOICES = {
#         ZEROU: "Zerou",
#         CLIENTE_PROPRIETARIO: "Cliente Proprietario",
#         PARCEIRO: "Parceiro",
#     }
#     tipo_responsavel = models.IntegerField(
#         help_text="Situação",
#         db_comment="",
#         verbose_name="Situação",
#         choices=STATUS_CHOICES,
#         default=EM_CADASTRO
#     )
#     nome_responsavel = models.CharField(
#         max_length=150,
#         help_text="Nome do Responsavel pela Carteira",
#         db_comment="Nome do Responsavel pela Carteira",
#         verbose_name="Nome do Responsavel pela Carteira",
#     )

#     get_quantidade_contratos(self)
#     get_valor_total(self)
#     get_valor_atualizado(self)
#     get_percentual_recuperacao(self)

    TIMEZONE_1 = 1
    TIMEZONE_2 = 2
    TIMEZONE_3 = 3
    TIMEZONE_4 = 4
    TIMEZONE_CHOICES = {
        TIMEZONE_1: "Fuso -1",
        TIMEZONE_2: "Fuso -2",
        TIMEZONE_3: "Fuso -3",
        TIMEZONE_4: "Fuso -4",
    }

#     dias_uteis
#     horario_inicio
#     horario_fim

#     duracao_padrao_atendimento_min
#     capacidade_default_diaria
#     capacidade_default_simultanea
#     tempo_inatividade_min
#     politica_redistribuicao MANUAL
#     retencao_interacoes_dias

    def save(self, *args, **kwargs):
        # TODO 202608202215 uppercase para o nome
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.id} - {self.nome}"
    class Meta:
        #abstract = True
        db_table = "carteiras"
        verbose_name = "Carteira"
        verbose_name_plural = "Carteiras"
        db_table_comment = "Carteiras"
        permissions = (
            ('import_carteiras', 'Can import'),
            ('export_carteiras', 'Can export')
        )
