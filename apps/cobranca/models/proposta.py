from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

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
        help_text="% Entrada",
        db_comment="% Entrada",
        verbose_name="% Entrada",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
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

    def trigger_before_insert_or_update_set_parcelas(self):
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

        soma_valor_atualizado = soma_de_todas_as_parcelas_de_todos_os_contratos

        if self.modalidade == self.PARCELADO and self.qtd_parcelas:
            valor_entrada = (soma_valor_atualizado * (self.entrada/100))

            PropostasParcelas.objects.create(
                proposta=self,
                numero_parcela=0,
                data_vencimento=date.today() + timedelta(days=3),
                valor=valor_entrada
            )

            soma_valor_atualizado = ( soma_valor_atualizado - valor_entrada ) / self.qtd_parcelas
            for i in range(self.qtd_parcelas):
                PropostasParcelas.objects.create(
                    proposta=self,
                    numero_parcela=i+1,
                    data_vencimento=(date.today() + relativedelta(months=(i+1))) if i+1 != 1 else (date.today() + timedelta(days=34)),
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

    # TODO 202608201522 validar se já existe proposta já aceita
    # se ja existe então não pode ter outro acordo

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
                raise ValidationError({
                    "entrada": f"A entrada deve ser maior ou igual a entrada minima de {regras_negociacao.entrada_minima}%"
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
        self.trigger_before_insert_or_update_set_parcelas()
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
