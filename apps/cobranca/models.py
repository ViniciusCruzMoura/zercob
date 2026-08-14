from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Carteiras(models.Model):
    id = models.BigAutoField(primary_key=True)

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
    observacao = models.TextField(
        max_length=3000,
        help_text="Observação",
        db_comment="Observação",
        verbose_name="Observação",
    )

    nome_cliente_proprietario = models.CharField(
        max_length=150,
        help_text="Nome Cliente Proprietario",
        db_comment="Nome Cliente Proprietario",
        verbose_name="Nome Cliente Proprietario",
    )
#     usuario_responsavel
    nome_empresa_responsavel = models.CharField(
        max_length=150,
        help_text="Nome Empresa Responsavel",
        db_comment="Nome Empresa Responsavel",
        verbose_name="Nome Empresa Responsavel",
    )


    def __str__(self):
        return f"{self.id} - {self.nome_empresa_responsavel}"
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

class Contratos(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    def __str__(self):
        return f"{self.id}"
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

class Propostas(models.Model):
    id = models.BigAutoField(primary_key=True)
    contrato = models.ForeignKey(
        Contratos,
        on_delete=models.CASCADE,
    )

    data_inclusao = models.DateField(
        help_text="Data da Decisão: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        db_comment="Data da Decisão: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data da Decisão",
        db_index=True,
        null=True,
        blank=True,
    )

    APROVADO = 1
    REJEITADO = 2
    DECISAO_CHOICES = {
        APROVADO: "Aprovado",
        REJEITADO: "Rejeitado",
    }
    decisao = models.IntegerField(
        help_text="Situação",
        db_comment="",
        verbose_name="Situação",
        choices=DECISAO_CHOICES,
        null=True,
        blank=True,
    )
    data_decisao = models.DateField(
        help_text="Data da Decisão: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        db_comment="Data da Decisão: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data da Decisão",
        db_index=True,
        null=True,
        blank=True,
    )
    usuario_decisao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text="Decisor",
        db_comment="Decisor",
        verbose_name="Decisor"
    )
    observacao = models.TextField(
        max_length=3000,
        help_text="Observação",
        db_comment="Observação",
        verbose_name="Observação",
    )

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

# class PropostasNegociadas(models.Model):
#     pass

class DevedoresParecelas(models.Model):
    A_VENCER = 1
    PAGO = 2
    QUEBRA = 3
    CANCELADO = 4
    STATUS_CHOICES = {
        A_VENCER: "A vencer",
        PAGO: "Pago",
        QUEBRA: "Quebra",
        CANCELADO: "Cancelado",
    }
    id = models.BigAutoField(primary_key=True)
    devedor = models.ForeignKey(
        'Devedores',
        on_delete=models.CASCADE,
        related_name='parcelas',
        help_text="Referência à Devedores"
    )
    status = models.IntegerField(
        help_text="Situação",
        db_comment="1 - A vencer, 2 - Pago, 3 - Quebra",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
        default=A_VENCER
    )
    parcela_inicio = models.IntegerField(
        help_text="Parcela Inicial",
        db_comment="Parcela Inicial",
        verbose_name="Parcela Inicial",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(120),
        ],
        null=True,
        blank=True,
    )
    parcela_final = models.IntegerField(
        help_text="Parcela Final",
        db_comment="Parcela Final",
        verbose_name="Parcela Final",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(120),
        ],
        null=True,
        blank=True,
    )
    valor_apagar = models.IntegerField(
        help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor A pagar",
        verbose_name="Valor A pagar",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    valor_pago = models.IntegerField(
        help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor Pago",
        verbose_name="Valor Pago",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    saldo = models.IntegerField(
        help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor do Saldo",
        verbose_name="Valor do Saldo",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "devedores_parecelas"
        verbose_name = "Parcela do Devedor"
        verbose_name_plural = "Parcelas do Devedor"
        db_table_comment = "Parcelas do Devedor"
        permissions = (
            ('import_devedoresparcelas', 'Can import'),
            ('export_devedoresoarcelas', 'Can export')
        )

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
    WHATSAPP = 2
    EMAIL = 3
    OUTRO = 4
    TIPO_CHOICES = {
        TELEFONE: "Telefone",
        WHATSAPP: "Whatsapp",
        EMAIL: "Email",
    }
    tipo = models.IntegerField(
        help_text="Situação",
        db_comment="1 - A vencer, 2 - Pago, 3 - Quebra",
        verbose_name="Situação",
        choices=TIPO_CHOICES,
        default=OUTRO,
    )
    contato = models.CharField(
        max_length=500,
        help_text="Contato",
        db_comment="Contato",
        verbose_name="Contato",
    )
    observacao = models.TextField(
        max_length=3000,
        help_text="Observação",
        db_comment="Observação",
        verbose_name="Observação",
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
    )
#     carteira
    numero_contrato = models.CharField(
        max_length=300,
        help_text="Numero do Contrato",
        db_comment="Numero do Contrato",
        verbose_name="Numero do Contrato",
        db_index=True,
    )
    saldo = models.IntegerField(
        help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor do Saldo",
        verbose_name="Valor do Saldo",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    titulo = models.CharField(
        max_length=300,
        help_text="Titulo",
        db_comment="Titulo",
        verbose_name="Titulo",
        db_index=True,
    )

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

class AcordosParcelas(models.Model):
    A_VENCER = 1
    PAGO = 2
    QUEBRA = 3
    CANCELADO = 4
    STATUS_CHOICES = {
        A_VENCER: "A vencer",
        PAGO: "Pago",
        QUEBRA: "Quebra",
        CANCELADO: "Cancelado",
    }
    id = models.BigAutoField(primary_key=True)
    acordo = models.ForeignKey(
        'Acordos',
        on_delete=models.CASCADE,
        related_name='parcelas',
        help_text="Referência à Acordos"
    )
    status = models.IntegerField(
        help_text="Situação",
        db_comment="1 - A vencer, 2 - Pago, 3 - Quebra",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
        default=A_VENCER
    )
    parcela_inicio = models.IntegerField(
        help_text="Parcela Inicial",
        db_comment="Parcela Inicial",
        verbose_name="Parcela Inicial",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(120),
        ],
        null=True,
        blank=True,
    )
    parcela_final = models.IntegerField(
        help_text="Parcela Final",
        db_comment="Parcela Final",
        verbose_name="Parcela Final",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(120),
        ],
        null=True,
        blank=True,
    )
    valor_apagar = models.IntegerField(
        help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor A pagar",
        verbose_name="Valor A pagar",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    valor_pago = models.IntegerField(
        help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor Pago",
        verbose_name="Valor Pago",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    saldo = models.IntegerField(
        help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor do Saldo",
        verbose_name="Valor do Saldo",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "acordos_parecelas"
        verbose_name = "Parcela do Acordo"
        verbose_name_plural = "Parcelas do Acordo"
        db_table_comment = "Parcelas do Acordo"
        permissions = (
            ('import_devedoresparcelas', 'Can import'),
            ('export_devedoresoarcelas', 'Can export')
        )

class AcordosPagamentos(models.Model):
    PENDENTE = 1
    ESTORNADO = 2
    CONCILIADO = 3
    STATUS_CHOICES = {
        ESTORNADO: "Estornado",
        CONCILIADO: "Conciliado",
        PENDENTE: "Pendente",
    }
    PIX = 1
    BOLETO = 2
    METODO_PAGAMENTO_CHOICES = {
        PIX: "Pix",
        BOLETO: "Boleto",
    }
    id = models.BigAutoField(primary_key=True)
    acordo = models.ForeignKey(
        'Acordos',
        on_delete=models.CASCADE,
        related_name='pagamentos',
        help_text="Referência à Acordos"
    )
    status = models.IntegerField(
        help_text="Situação",
        db_comment="1 - A vencer, 2 - Pago, 3 - Quebra",
        verbose_name="Situação",
        choices=STATUS_CHOICES,
        default=PENDENTE
    )
    metodo_pagamento = models.IntegerField(
        help_text="Metodo de Pagamento",
        db_comment=" ",
        verbose_name="Metodo de Pagamento",
        choices=METODO_PAGAMENTO_CHOICES,
        default=PIX
    )
    valor_pago = models.IntegerField(
        help_text="Sem separadores de milhares e sem vírgula. É obrigatório sempre informar as casas decimais, ainda que seu valor seja “00” Exemplo: 128088 deve ser informado para o número R$ 1280,88",
        db_comment="Valor Pago",
        verbose_name="Valor Pago",
        validators=[
            MinValueValidator(100)
        ],
        null=True,
        blank=True,
    )
    data_pagamento = models.DateField(
        help_text="Data do Pagamento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        db_comment="Data do Pagamento: AAAA-MM-DD; A: Ano com 4 caracteres M: Mês com 2 caracteres D: Dia com 2 caracteres",
        verbose_name="Data do Pagamento",
        db_index=True,
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "acordos_pagamentos"
        verbose_name = "Pagamento do Acordo"
        verbose_name_plural = "Pagamentos do Acordo"
        db_table_comment = "Pagamentos do Acordo"
        permissions = (
            ('import_acordospagamentos', 'Can import'),
            ('export_acordospagamentos', 'Can export')
        )

class Acordos(models.Model):
    id = models.BigAutoField(primary_key=True)
    devedor = models.ForeignKey(
        Devedores, 
        on_delete=models.PROTECT, 
        blank=True,
        null=True,
        help_text="Devedor",
        db_comment="Devedor",
        verbose_name="Devedor",
    )

# -devedor(tabela Devedores) 1 para N
# -lista de parcelas negociada(tabela AcordoParcelas) 1 para N
# -?instrução pagamento
# -?registro pagamento
# -pagamento (tabela Pagamento)

    def __str__(self):
        return f"{self.id}"
    class Meta:
        #abstract = True
        db_table = "acorodos"
        verbose_name = "Acordos"
        verbose_name_plural = "Acordos"
        db_table_comment = "Acordos"
        permissions = (
            ('import_acordos', 'Can import'),
            ('export_acordos', 'Can export'),
            ('viewall_acordos', 'Can view all Arquivo do Solfacil Acordo'),
        )
