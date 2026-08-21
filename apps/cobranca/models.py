from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

# class OperacoesParametros(models.Model):
#     id = models.BigAutoField(primary_key=True)

# class CarteirasOperacoes(models.Model):
#     id = models.BigAutoField(primary_key=True)

# 1 carteira pode ter N operações
# 1 operação pode ter 1 parametros


# carteira (agrupador de contratos de uma operação).

# class ContratoDebito
# class ContratoDebitoParcela
# existe um devido(divida) e esta divida pode ter N parcelas

# class ContratosNotificacao(models.Models):
#     id = models.BigAutoField(primary_key=True)




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
