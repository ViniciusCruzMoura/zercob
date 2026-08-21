from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from apps.cobranca.models.carteira import Carteiras, CarteirasRegrasNegociacao

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
            multa = 0
            juros = 0
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
