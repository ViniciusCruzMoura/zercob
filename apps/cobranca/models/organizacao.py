from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class UsuarioOrganizacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    organizacao = models.ForeignKey(
        'Organizacao',
        verbose_name="Organização",
        on_delete=models.PROTECT,
    )
    usuario = models.ForeignKey(
        User,
        verbose_name="Usuario",
        on_delete=models.PROTECT,
    )
    @property
    def get_usuario_name(self):
        if self.usuario:
            return self.usuario.name
        return "-"
    @property
    def get_usuario_email(self):
        if self.usuario:
            return self.usuario.email
        return "-"
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "usuario_organizacao"
        verbose_name = "Organização do Usuario"
        verbose_name_plural = "Organizações do Usuario"
        db_table_comment = "Organizações do Usuario"
        permissions = (
            ('import_usuarioorganizacao', 'Can import'),
            ('export_usuarioorganizacao', 'Can export')
        )

class OrganizacaoRegrasCobranca(models.Model):
    id = models.BigAutoField(primary_key=True)
    organizacao = models.ForeignKey(
        'Organizacao',
        on_delete=models.PROTECT,
    )
    atraso = models.IntegerField(
        help_text="Dias em Atraso",
        db_comment="Dias em Atraso",
        verbose_name="Dias em Atraso",
        validators=[
            MinValueValidator(-30),
            MaxValueValidator(3650),
        ],
        null=True,
        blank=True,
    )
    SMS = 1
    EMAIL = 2
    WHATSAPP = 3
    DISCADOR = 4
    TIPO_ACAO_CHOICES = {
        SMS: "SMS",
        EMAIL: "Email",
        WHATSAPP: "Whatsapp",
        DISCADOR: "Discador",
    }
    tipo_acao = models.IntegerField(
        help_text="Situação",
        db_comment="Situação",
        verbose_name="Situação",
        choices=TIPO_ACAO_CHOICES,
        default=SMS
    )
    SEM_TEXTO = 1
    AVISO_PRE_VENCIMENTO = 2
    COBRANCA_AMIGAVEL = 3
    PROPOSTA_ACORDO = 4
    MODELO_MENSAGEM_CHOICES = {
        SEM_TEXTO: "Sem texto",
        AVISO_PRE_VENCIMENTO: "Aviso pré-vencimento",
        COBRANCA_AMIGAVEL: "Cobrança amigavel",
        PROPOSTA_ACORDO: "Proposta de Acordo",
    }
    modelo_mensagem = models.IntegerField(
        help_text="Modelo de Mensagem",
        db_comment="Modelo de Mensagem",
        verbose_name="Modelo de Mensagem",
        choices=MODELO_MENSAGEM_CHOICES,
        default=SEM_TEXTO
    )

    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "organizacao_regras_cobranca"
        verbose_name = "Regra de Cobrança"
        verbose_name_plural = "Regras de Cobrança"
        db_table_comment = "Regras de Cobrança"
        permissions = (
            ('import_organizacaoregrascobranca', 'Can import'),
            ('export_organizacaoregrascobranca', 'Can export')
        )

class Organizacao(models.Model):
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
    )
    razao_social = models.CharField(
        max_length=150,
        help_text="Razão Social",
        db_comment="Razão Social",
        verbose_name="Razão Social",
    )
    nome_fantasia = models.CharField(
        max_length=150,
        help_text="Nome Fantasia",
        db_comment="Nome Fantasia",
        verbose_name="Nome Fantasia",
    )
    endereco = models.CharField(
        max_length=150,
        help_text="Endereço",
        db_comment="Endereço",
        verbose_name="Endereço",
    )
    telefone = models.CharField(
        max_length=17,
        help_text="Telefone",
        db_comment="Telefone",
        verbose_name="Telefone",
        validators=[
            RegexValidator(
                regex=r'^\+55\s\d{2}\s\d{4,5}-\d{4}$',
                message='Numero de Telefone Invalido. Padrão: +55 DDD XXXXX-XXXX'
            )
        ],
    )
    email_institucional = models.CharField(
        max_length=256,
        help_text="Email Institucional",
        db_comment="Email Institucional",
        verbose_name="Email Institucional",
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
                message='Email Invalido.'
            )
        ],
    )
    def save(self, *args, **kwargs):
        # TODO 202608202214 razao_social, fantasia, endereco
        # como uppercase
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.nome_fantasia} ({self.cpf_cnpj})"
    class Meta:
        #abstract = True
        db_table = "organizacao"
        verbose_name = "Organização"
        verbose_name_plural = "Organizações"
        db_table_comment = "Organizações"
        permissions = (
            ('import_clienteorganizacao', 'Can import'),
            ('export_clienteorganizacao', 'Can export')
        )
