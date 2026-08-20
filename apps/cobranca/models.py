from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError

# class OperacoesParametros(models.Model):
#     id = models.BigAutoField(primary_key=True)

# class CarteirasOperacoes(models.Model):
#     id = models.BigAutoField(primary_key=True)

# 1 carteira pode ter N operações
# 1 operação pode ter 1 parametros

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
    )
    multa = models.IntegerField(
        help_text="% de Multa",
        db_comment="% Multa",
        verbose_name="% Multa",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
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
        null=True,
        blank=True,
    )
    entrada_minima = models.IntegerField(
        help_text="Entrada Minima para o Acordo",
        db_comment="Entrada Minima para o Acordo",
        verbose_name="Entrada Minima para o Acordo",
        validators=[
            MinValueValidator(0),
        ],
        null=True,
        blank=True,
    )
    maximo_parcelas = models.IntegerField(
        help_text="Quantidade Maxima de Parcelas",
        db_comment="Quantidade Maxima de Parcelas",
        verbose_name="Quantidade Maxima de Parcelas",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(420),
        ],
        null=True,
        blank=True,
    )

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

# carteira (agrupador de contratos de uma operação).
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

    responsavel = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text="Responsavel pela Carteira",
        db_comment="Responsavel pela Carteira",
        verbose_name="Responsavel pela Carteira",
    )
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
    nome_responsavel = models.CharField(
        max_length=150,
        help_text="Nome do Responsavel pela Carteira",
        db_comment="Nome do Responsavel pela Carteira",
        verbose_name="Nome do Responsavel pela Carteira",
    )

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

# class ContratoDebito
# class ContratoDebitoParcela
# existe um devido(divida) e esta divida pode ter N parcelas

# class ContratosNotificacao(models.Models):
#     id = models.BigAutoField(primary_key=True)

class ContratosParcelas(models.Model):
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

    contrato = models.ForeignKey(
        'Contratos',
        on_delete=models.CASCADE,
    )
    numero_parcela = models.IntegerField(
#         help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="N° Parcela",
        verbose_name="N° Parcela",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(420),
        ],
        null=True,
        blank=True,
    )
    data_vencimento = models.DateField(
#         help_text="Data do Pagamento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        db_comment="Data do Vencimento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data do Vencimento",
        db_index=True,
        null=True,
        blank=True,
    )
#     data_vencimento_original = models.DateField(
# #         help_text="Data do Pagamento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
#         db_comment="Data do Vencimento Original: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
#         verbose_name="Data do Vencimento Original",
#         db_index=True,
#         null=True,
#         blank=True,
#     )
    data_pagamento = models.DateField(
#         help_text="Data do Pagamento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        db_comment="Data do Pagamento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data do Pagamento",
        db_index=True,
        null=True,
        blank=True,
    )
    valor_original = models.IntegerField(
#         help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor da Parcela",
        verbose_name="Valor da Parcela",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    valor_atualizado = models.IntegerField(
#         help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor Atualizado (Juros + Multa)",
        verbose_name="Valor (Juros + Multa)",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
#     valor_pago = models.IntegerField(
# #         help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
#         db_comment="Valor Pago",
#         verbose_name="Valor Pago",
#         validators=[
#             MinValueValidator(100)
#         ],
#         null=True,
#         blank=True,
#     )

    A_VENCER = 1
    VENCIDO = 2
    PAGO = 3
    STATUS_CHOICES = {
        A_VENCER: "A vencer",
        VENCIDO: "Vencido",
        PAGO: "Pago",
    }
    status = models.IntegerField(
        help_text="Situação",
        db_comment="Situação",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
        default=A_VENCER
    )

    atraso = models.IntegerField(
        help_text="Dias em Atraso",
        db_comment="Dias em Atraso",
        verbose_name="Dias em Atraso",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3650),
        ],
#         null=True,
#         blank=True,
    )

    def get_dias_em_atraso(self):
        hoje = datetime.now()

        data_vencimento = self.data_vencimento
#         data_vencimento_original = self.data_vencimento_original
        data_pagamento = self.data_pagamento
        
        if hoje and isinstance(hoje, datetime):
            hoje = hoje.date()

        if data_vencimento and isinstance(data_vencimento, datetime):
            data_vencimento = data_vencimento.date()

#         if data_vencimento_original and isinstance(data_vencimento_original, datetime):
#             data_vencimento_original = data_vencimento_original.date()

        if data_pagamento and isinstance(data_pagamento, datetime):
            data_pagamento = data_pagamento.date()

        if self.status == self.PAGO:
            return (data_pagamento - data_vencimento).days

        elif self.status == self.VENCIDO:
            return (hoje - data_vencimento).days
        
        elif self.status == self.A_VENCER:
            return (hoje - data_vencimento).days

        return 0

    def display_valor_atualizado(self):
        from apps.common.guias import guias_formatar_valor
        return guias_formatar_valor(self.valor_atualizado)

    def update_atraso(self):
        print("TODO 202608181023 update_atraso")
        self.atraso = self.get_dias_em_atraso()

    def update_status(self):
        print("TODO 202608181031 update_status")
        if self.get_dias_em_atraso() > 0:
            self.status = self.VENCIDO

    def update_valor_atualizado(self):
        print("TODO 202608181024 update_valor_atualizado")
        if not self.id:
            self.valor_atualizado = self.valor_original
        if self.get_dias_em_atraso() > 0:
            regras_negociacao = (
                CarteirasRegrasNegociacao
                .objects
                .filter(carteira=self.contrato.carteira_id)
                .last()
            )
            if regras_negociacao.parcelas:
                multa = (self.valor_original * (regras_negociacao.multa/100)) * self.get_dias_em_atraso() // 30
                juros = self.valor_original * (regras_negociacao.juros/100)
            self.valor_atualizado = self.valor_original + multa + juros

    def save(self, *args, **kwargs):
        #if self._state.adding: print("INSERT")
        from apps.common.admin_model import admin_model_save
        admin_model_save(self, [], [], *args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "contratos_parcelas"
        verbose_name = "Parcela em Debito do Contrato"
        verbose_name_plural = "Parcelas em Debido do Contrato"
        db_table_comment = "Parcelas em Debido do Contrato"
        permissions = (
            ('import_contratosparcelasdebito', 'Can import'),
            ('export_contratosparcelasdebito', 'Can export')
        )

class Contratos(models.Model):
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

    carteira = models.ForeignKey(
        Carteiras,
        on_delete=models.CASCADE,
    )
    devedor = models.ForeignKey(
        'Devedores', 
        on_delete=models.PROTECT, 
        help_text="Devedor",
        db_comment="Devedor",
        verbose_name="Devedor",
    )
    produto = models.CharField(
        max_length=300,
        help_text="Produto",
        db_comment="Produto",
        verbose_name="Produto",
    )

    ATIVO = 1
    LIQUIDADO = 2
    RENEGOCIADO = 3
    CANCELADO = 4
    SUSPENSO = 5
    JUDICIALIZADO = 6
    BAIXADO = 7
    STATUS_CHOICES = {
        ATIVO: "Ativo",
        LIQUIDADO: "Liquidado",
        RENEGOCIADO: "Renegociado",
        CANCELADO: "Cancelado",
        SUSPENSO: "Suspenso",
        JUDICIALIZADO: "Judicializado",
        BAIXADO: "Baixado",
    }
    status = models.IntegerField(
        help_text="Situação",
        db_comment="Situação",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
    )

#     status
#     valor_original
#     saldo_devedor
#     valor_atualizado

#     data_vencimento
#     data_vencimento_original

    def __str__(self):
        return f"{self.id} | {self.devedor} | {self.carteira}"
    class Meta:
        #abstract = True
        db_table = "contratos"
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        db_table_comment = "Contratos"
        permissions = (
            ('import_contratos', 'Can import'),
            ('export_contratos', 'Can export')
        )

class PropostasParcelas(models.Model):
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

    proposta = models.ForeignKey(
        'Propostas',
        on_delete=models.CASCADE,
    )

    numero_parcela = models.IntegerField(
        db_comment="N° Parcela",
        verbose_name="N° Parcela",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(420),
        ],
        null=True,
        blank=True,
    )
    data_vencimento = models.DateField(
        db_comment="Data do Vencimento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data do Vencimento",
        db_index=True,
        null=True,
        blank=True,
    )
    valor = models.IntegerField(
        db_comment="Valor da Parcela",
        verbose_name="Valor da Parcela",
        validators=[
            MinValueValidator(0)
        ],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "propostas_parcelas"
        verbose_name = "Parcela da Proposta"
        verbose_name_plural = "Parcelas da Proposta"
        db_table_comment = "Parcelas da Proposta"
        permissions = (
            ('import_propostasparcelas', 'Can import'),
            ('export_propostasparcelas', 'Can export')
        )

class PropostaContrato(models.Model):
    id = models.BigAutoField(primary_key=True)
    proposta = models.ForeignKey("Propostas", on_delete=models.CASCADE)
    contrato = models.ForeignKey("Contratos", on_delete=models.CASCADE)
#     data_associacao = models.DateField(auto_now_add=True)
#     status = models.CharField(max_length=50)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # disparar as triggers da tabela Propostas
        self.proposta.save()
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "proposta_contrato"
        verbose_name = "Contrato da Proposta"
        verbose_name_plural = "Contratos das Propostas"
        db_table_comment = "Contratos das Propostas"
        permissions = (
            ('import_propostacontrato', 'Can import'),
            ('export_propostacontrato', 'Can export')
        )
        constraints = [
            models.UniqueConstraint(
                fields=["proposta", "contrato"],
                name="unique_proposta_contrato",
            )
        ]

class Propostas(models.Model):
    id = models.BigAutoField(primary_key=True)

#     contratos = models.ManyToManyField(
#         "Contratos",
#         related_name="propostas",
# #         null=True,
# #         blank=True,
#     )
    devedor = models.ForeignKey(
        'Devedores', 
        on_delete=models.PROTECT, 
        help_text="Devedor",
        db_comment="Devedor",
        verbose_name="Devedor",
    )

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
    entrada = models.IntegerField(
        help_text="Entrada para o Acordo",
        db_comment="Entrada para o Acordo",
        verbose_name="Entrada para o Acordo",
        validators=[
            MinValueValidator(0),
        ],
        null=True,
        blank=True,
    )
    qtd_parcelas = models.IntegerField(
        help_text="Quantidade de Parcelas",
        db_comment="Quantidade de Parcelas",
        verbose_name="Quantidade de Parcelas",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(420),
        ],
        null=True,
        blank=True,
    )

    RASCUNHO = 1
    AGUARDANDO_ACEITE = 2
    RECUSADA = 3
    EXPIRADA = 4
    ACEITO = 5
    STATUS_CHOICES = {
        RASCUNHO: "Rascunho",
        AGUARDANDO_ACEITE: "Aguardando Aceite",
        RECUSADA: "Recusada",
        EXPIRADA: "Expirada",
        ACEITO: "Aceito",
    }
    status = models.IntegerField(
        help_text="Situação",
        db_comment="",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
        default=RASCUNHO
    )

    def trigger_before_insert_or_updatre_set_parcelas(self):
        if self.modalidade == self.A_VISTA:
            self.entrada = 0
            self.qtd_parcelas = 1
        elif self.modalidade == self.PARCELADO:
            pass # fazer nada por agora

    def trigger_after_insert_or_update_calc_parcelas(self):
        # TODO 202608200014 esta trigger deveria ser executada na tabela PropostaContrato ?
        #if not self.id:
        #    return
        # def proc_calc_parcelas(self, in_proposta_id, in_modalidade, in_qtd_parcelas)
        #in_proposta_id = self.id
        #in_modalidade = self.modalidade
        #in_qtd_parcelas = self.qtd_parcelas
        #out_proposta_type = self

        PropostasParcelas.objects.filter(proposta_id=self.id).delete()
        
        soma_de_todas_as_parcelas_de_todos_os_contratos = 0

        # TODO 202608192241 garantir que exista os contratos já
        # persistidos no db ou pegar da memoria.
        # os contratos deve ser persistidos primeiro antes de chegar aqui
        # isso deveria ser executado apos o save da PropostaContrato
        contratos_da_proposta = PropostaContrato.objects.filter(proposta_id=self.id)
        for contrato_da_proposta in contratos_da_proposta:
            contrato = contrato_da_proposta.contrato
            # TODO 202608192306 todas as carteira tem q estar na mesma
            # carteira? se nao, regra de qual carteira deve ser utilizada?
            parcelas = ContratosParcelas.objects.filter(contrato_id=contrato.id)
            soma_das_parcelas = 0
            for parcela in parcelas:
                # TODO 202608192249 se nao existe valor_atualizado então
                # calcular e persistir
                soma_das_parcelas += parcela.valor_atualizado
            soma_de_todas_as_parcelas_de_todos_os_contratos += soma_das_parcelas

#         parcelas = ContratosParcelas.objects.filter(contrato_id=self.contrato.id)
#         soma_valor_atualizado = 0
#         for parcela in parcelas:
#             soma_valor_atualizado += parcela.valor_atualizado
        soma_valor_atualizado = soma_de_todas_as_parcelas_de_todos_os_contratos

        if self.modalidade == self.PARCELADO and self.qtd_parcelas:
            PropostasParcelas.objects.create(
                proposta=self,
                numero_parcela=0,
                data_vencimento=date.today() + timedelta(days=3),
                valor=self.entrada
            )
            soma_valor_atualizado = (soma_valor_atualizado - self.entrada) / self.qtd_parcelas
            for i in range(self.qtd_parcelas):
                PropostasParcelas.objects.create(
                    proposta=self,
                    numero_parcela=i+1,
                    data_vencimento=date.today() + timedelta(days=30*(i+1) if i+1 != 1 else 33*(i+1)),
                    valor=soma_valor_atualizado
                )
        elif self.modalidade == self.A_VISTA:
            contrato_da_proposta = contratos_da_proposta.last()
            contrato = contrato_da_proposta.contrato if contrato_da_proposta else None
            regras_negociacao = (
                CarteirasRegrasNegociacao
                .objects
                .filter(carteira_id=contrato.carteira.id if contrato else None)
                .last()
            )
            porcentual_de_desconto = regras_negociacao.desconto / 100 if regras_negociacao else 0
            soma_valor_atualizado -= soma_valor_atualizado * porcentual_de_desconto
            PropostasParcelas.objects.create(
                proposta=self,
                numero_parcela=1,
                data_vencimento=date.today() + timedelta(days=3),
                valor=soma_valor_atualizado
            )

    def trigger_after_insert_or_update_do_acordo(self):
        if self.status == self.ACEITO:
            print("TODO 202608200044 inserir registro no acordos caso não exista")

    def validate_entrada(self):
        if self.modalidade == self.PARCELADO:
            contratos_da_proposta = PropostaContrato.objects.filter(proposta_id=self.id)
            contrato_da_proposta = contratos_da_proposta.last()
            contrato = contrato_da_proposta.contrato if contrato_da_proposta else None
            regras_negociacao = (
                CarteirasRegrasNegociacao
                .objects
                .filter(carteira_id=contrato.carteira.id if contrato else None)
                .last()
            )
            if self.entrada < regras_negociacao.entrada_minima:
                from apps.common.guias import guias_formatar_valor
                raise ValidationError({
                    "entrada": f"A entrada deve ser maior ou igual a entrada minima de {guias_formatar_valor(regras_negociacao.entrada_minima)}"
                })

    def validate_qtd_parcelas(self):
        if self.modalidade == self.PARCELADO:
            contratos_da_proposta = PropostaContrato.objects.filter(proposta_id=self.id)
            contrato_da_proposta = contratos_da_proposta.last()
            contrato = contrato_da_proposta.contrato if contrato_da_proposta else None
            regras_negociacao = (
                CarteirasRegrasNegociacao
                .objects
                .filter(carteira_id=contrato.carteira.id if contrato else None)
                .last()
            )
            if self.qtd_parcelas > regras_negociacao.maximo_parcelas:
                raise ValidationError({
                    "qtd_parcelas": f"A quantidade de parcelas deve ser maior ou igual a parcela maxima de {regras_negociacao.maximo_parcelas}"
                })


    def clean(self):
        super().clean()
        # django rest use model clean method
        # trigger before insert or update proc_validate(self)
        # deve conter ao menos 1 contrato
        self.validate_entrada()
        self.validate_qtd_parcelas()

    def save(self, *args, **kwargs):
        from apps.common.admin_model import admin_model_save
        admin_model_save(self, [], [], *args, **kwargs)
        self.trigger_before_insert_or_updatre_set_parcelas()
        super().save(*args, **kwargs)
        self.trigger_after_insert_or_update_calc_parcelas()
        self.trigger_after_insert_or_update_do_acordo()
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "propostas"
        verbose_name = "Proposta"
        verbose_name_plural = "Propostas"
        db_table_comment = "Propostas"
        permissions = (
            ('import_propostas', 'Can import'),
            ('export_propostas', 'Can export')
        )
        # Methods like QuerySet.bulk_create() or QuerySet.update()
        #never call save(), clean(), or pre_save signals. Only Database Constraints
#         constraints = [
#             models.CheckConstraint(
#                 condition=Q(discounted_price__lte=F('price')),
#                 name='discount_less_than_or_equal_to_price'
#             )
#         ]

# class PropostasNegociadas(models.Model):
#     pass

# class DevedoresParecelas(models.Model):
#     A_VENCER = 1
#     PAGO = 2
#     QUEBRA = 3
#     CANCELADO = 4
#     STATUS_CHOICES = {
#         A_VENCER: "A vencer",
#         PAGO: "Pago",
#         QUEBRA: "Quebra",
#         CANCELADO: "Cancelado",
#     }
#     id = models.BigAutoField(primary_key=True)
#     devedor = models.ForeignKey(
#         'Devedores',
#         on_delete=models.CASCADE,
#         related_name='parcelas',
#         help_text="Referência à Devedores"
#     )
#     status = models.IntegerField(
#         help_text="Situação",
#         db_comment="1 - A vencer, 2 - Pago, 3 - Quebra",
#         verbose_name="Situação",
#         choices=STATUS_CHOICES,
#         default=A_VENCER
#     )
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
#     def __str__(self):
#         return f"{self.id}"
#     class Meta:
#         #abstract = True
#         db_table = "devedores_parecelas"
#         verbose_name = "Parcela do Devedor"
#         verbose_name_plural = "Parcelas do Devedor"
#         db_table_comment = "Parcelas do Devedor"
#         permissions = (
#             ('import_devedoresparcelas', 'Can import'),
#             ('export_devedoresoarcelas', 'Can export')
#         )

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

# class AcordosPagamentos(models.Model):
#     PENDENTE = 1
#     ESTORNADO = 2
#     CONCILIADO = 3
#     STATUS_CHOICES = {
#         ESTORNADO: "Estornado",
#         CONCILIADO: "Conciliado",
#         PENDENTE: "Pendente",
#     }
#     PIX = 1
#     BOLETO = 2
#     METODO_PAGAMENTO_CHOICES = {
#         PIX: "Pix",
#         BOLETO: "Boleto",
#     }
#     id = models.BigAutoField(primary_key=True)
#     acordo = models.ForeignKey(
#         'Acordos',
#         on_delete=models.CASCADE,
#         related_name='pagamentos',
#         help_text="Referência à Acordos"
#     )
#     status = models.IntegerField(
#         help_text="Situação",
#         db_comment="1 - A vencer, 2 - Pago, 3 - Quebra",
#         verbose_name="Situação",
#         choices=STATUS_CHOICES,
#         default=PENDENTE
#     )
#     metodo_pagamento = models.IntegerField(
#         help_text="Metodo de Pagamento",
#         db_comment=" ",
#         verbose_name="Metodo de Pagamento",
#         choices=METODO_PAGAMENTO_CHOICES,
#         default=PIX
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
#     data_pagamento = models.DateField(
#         help_text="Data do Pagamento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
#         db_comment="Data do Pagamento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
#         verbose_name="Data do Pagamento",
#         db_index=True,
#         null=True,
#         blank=True,
#     )
#     def __str__(self):
#         return f"{self.id}"
#     class Meta:
#         #abstract = True
#         db_table = "acordos_pagamentos"
#         verbose_name = "Pagamento do Acordo"
#         verbose_name_plural = "Pagamentos do Acordo"
#         db_table_comment = "Pagamentos do Acordo"
#         permissions = (
#             ('import_acordospagamentos', 'Can import'),
#             ('export_acordospagamentos', 'Can export')
#         )

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
        db_comment="Valor do Boleto",
        verbose_name="Valor do Boleto",
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


# TODO 202608191701
# pode ter varias simulações de propostas
# quando uma proposta for aceita, um acordo é firmado
# o acordo gerado com base a proposta, copiando os valores

# vários contratos por proposta
# somar a soma dos valores de todos os contratos
# 
# (acordo) so devedor pq proposta pode ter N contratos


# class Colchoes(models.Model):
#     pass
