from django.db import models
from apps.lgpd.salesforce import salesforce_buscar_parceiro_por_cpf
from apps.lgpd.pliq import pliq_cadastrar_contato
from datetime import datetime
from django.core.exceptions import ValidationError
from apps.lgpd.utils import validar_cpf

def validar_cgc_cpf(value):
    if not validar_cpf(value):
        raise ValidationError("CPF inválido.")

class SebraeParceiro(models.Model):
    cgc_cpf = models.CharField(
        primary_key=True,
        max_length=18,
        verbose_name="CGC/CPF",
        help_text="Número do CGC ou CPF.",
        validators=[validar_cgc_cpf]
    )
    account_id = models.CharField(
        blank=True, null=True,
        max_length=32,
        verbose_name="Código do Parceiro na FOCO",
        help_text="Código único do parceiro no FOCO."
    )
    cod_parceiro = models.BigIntegerField(
        blank=True, null=True,
        verbose_name="Código do Parceiro",
        help_text="Código único do parceiro."
    )
    cod_sebrae = models.IntegerField(
        verbose_name="Código SEBRAE",
        help_text="Código único do SEBRAE."
    )
    desc_sebrae = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name="Descrição SEBRAE",
        help_text="Descrição do SEBRAE."
    )
    numero = models.CharField(
        max_length=15,
        verbose_name="Número de Telefone",
        help_text="Número de Contato."
    )
    nome_razao_social = models.CharField(
        max_length=255,
        verbose_name="Nome/Razão Social",
        help_text="Nome ou razão social do parceiro."
    )
    cod_cid = models.IntegerField(
        blank=True, null=True,
        verbose_name="Código do Município",
        help_text="Código do município."
    )
    desc_cid = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name="Descrição do Município",
        help_text="Descrição do município."
    )
    cod_est = models.IntegerField(
        blank=True, null=True,
        verbose_name="Código do Estado",
        help_text="Código do estado."
    )
    desc_est = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name="Descrição do Estado",
        help_text="Descrição do estado."
    )
    situacao = models.IntegerField(
        blank=True, null=True,
        verbose_name="Situação",
        help_text="Situação do parceiro."
    )
    deficiencia = models.CharField(
        blank=True, null=True,
        max_length=1,
        verbose_name="Deficiência",
        help_text="Indica se há deficiência (S/N)."
    )
    sit_cadastral = models.CharField(
        blank=True, null=True,
        max_length=1,
        verbose_name="Situação Cadastral",
        help_text="Situação cadastral do parceiro."
    )
    desc_sit_cadastral = models.CharField(
        blank=True, null=True,
        max_length=50,
        verbose_name="Descrição da Situação Cadastral",
        help_text="Descrição da situação cadastral."
    )
    data_inclusao = models.DateTimeField(
        verbose_name="Data de Inclusão",
        help_text="Data em que o registro foi incluído."
    )
    data_ultima_alteracao = models.DateTimeField(
        blank=True, null=True,
        verbose_name="Data da Última Alteração",
        help_text="Data da última alteração no registro."
    )
    termo_aceite_lgpd = models.BooleanField(
        verbose_name="Termo de Aceite LGPD",
        help_text="Indica se o termo de aceite da LGPD foi aceito.",
        default=False
    )
    data_inclusao_termo_aceite_lgpd = models.DateTimeField(
        blank=True, null=True,
        verbose_name="Data de Inclusão do Termo de Aceite LGPD",
        help_text="Data em que o termo de aceite da LGPD foi incluído."
    )
    cod_sebrae_termo_aceite_lgpd = models.IntegerField(
        blank=True, null=True,
        verbose_name="Código SEBRAE do Termo de Aceite LGPD",
        help_text="Código do SEBRAE relacionado ao termo de aceite da LGPD."
    )
    desc_sebrae_termo_aceite_lgpd = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name="Descrição SEBRAE do Termo de Aceite LGPD",
        help_text="Descrição do SEBRAE relacionado ao termo de aceite da LGPD."
    )
    cod_parceiro_termo_aceite_lgpd = models.BigIntegerField(
        blank=True, null=True,
        verbose_name="Código do Parceiro do Termo de Aceite LGPD",
        help_text="Código do parceiro relacionado ao termo de aceite da LGPD."
    )
    nome_parceiro_termo_aceite_lgpd = models.CharField(
        blank=True, null=True,
        max_length=255,
        verbose_name="Nome do Parceiro do Termo de Aceite LGPD",
        help_text="Nome do parceiro relacionado ao termo de aceite da LGPD."
    )
    importacao_contato_pliq = models.BooleanField(
        blank=True, null=True,
        verbose_name="Importação do Contato na PliQ",
        help_text="Indica se a Importação do Contato para a PliQ foi realizado.",
        default=False
    )
    data_inclusao_importacao_pliq = models.DateTimeField(
        verbose_name="Data de Inclusão da Importação do Contato para a PliQ",
        help_text="Data em que a Importação do Contato para a PliQ foi incluído.",
        blank=True, null=True
    )
    qnt_vezes_importado_para_pliq = models.IntegerField(
        verbose_name="Quantidade de Vezes que foi Realizado a Importação do Contato na PliQ",
        help_text="Indica a Quantidade de Vezes que Ocorreu a Importação do Contato para a PliQ.",
        default=0
    )
    # TODO criar relacionamento para persistir o retorno da pliq quando a pesquisa for respondida
    # TODO criar campo onde diz se a origem dos dados é o SAS ou Salesforce

    def __str__(self):
        return self.nome_razao_social

    class Meta:
        verbose_name = "Parceiro SEBRAE"
        verbose_name_plural = "Parceiros SEBRAE"
        db_table_comment = "Tabela que armazena informações sobre parceiros do SEBRAE."
        db_table = "sebrae_parceiro"

    def clean(self):
        if validar_cpf(self.cgc_cpf):
            parceiro = salesforce_buscar_parceiro_por_cpf(self.cgc_cpf)
            if not parceiro or not parceiro.get("records"):
                raise ValidationError("Participante não localizado no FOCO.")

    def save(self, *args, **kwargs):
        if self.cgc_cpf and self.data_inclusao:
            super(SebraeParceiro, self).save(*args, **kwargs)
            return

        parceiro = salesforce_buscar_parceiro_por_cpf(self.cgc_cpf)
        for c in parceiro.get("records"):
            parceiro = c
            break
        self.cod_sebrae = 34 if not parceiro.get("CodigoSebrae__c") else parceiro.get("CodigoSebrae__c")
        self.desc_sebrae = "SEBRAE - MATO GROSSO DO SUL" if not parceiro.get("Sebrae__r.Name") else parceiro.get("Sebrae__r.Name")
        self.cgc_cpf = parceiro.get("CPF__c")
        self.account_id = parceiro.get("Id")
        self.cod_parceiro = 0
        self.numero = ''.join(i for i in parceiro.get("Phone") if i.isdigit()) if parceiro.get("Phone") else parceiro.get("Phone")
        self.nome_razao_social = parceiro.get("Name")
#         self.cod_cid = parceiro.get("CodCid", 1)
#         self.desc_cid = parceiro.get("DescCid", "1")
#         self.cod_est = parceiro.get("CodEst", 1)
#         self.desc_est = parceiro.get("DescEst", "1")
        self.cod_cid = 1
        self.desc_cid = "1"
        self.cod_est =  1
        self.desc_est = "1"
        self.situacao = 1 if parceiro.get("SituacaoCadastralSebrae__c") in ['Ativo'] else 0
        self.deficiencia = "N" if not parceiro.get("NecessidadeEspecial__c") else "S"
        self.sit_cadastral = "0" if not parceiro.get("SituacaoCadastral__c") else parceiro.get("SituacaoCadastral__c")
        self.desc_sit_cadastral = "Regular" if not parceiro.get("SituacaoCadastral__c") else parceiro.get("SituacaoCadastral__c")
        try:
            self.data_inclusao = datetime.strptime(parceiro.get("CreatedDate").split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
        except:
            pass
        try:
            self.data_ultima_alteracao = datetime.strptime(parceiro.get("LastModifiedDate").split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
        except:
            pass
        self.termo_aceite_lgpd = True if parceiro.get("TermoAceiteLGPD__c") in ['Sim', 'sim', 'SIM'] else False
        #self.data_inclusao_termo_aceite_lgpd = parceiro.get("DataInclusaoTermoAceiteLGPD")
        #self.cod_sebrae_termo_aceite_lgpd = parceiro.get("CodSebraeTermoAceiteLGPD")
        #self.desc_sebrae_termo_aceite_lgpd = parceiro.get("DescSebraeTermoAceiteLGPD")
        #self.cod_parceiro_termo_aceite_lgpd = parceiro.get("CodParceiroTermoAceiteLGPD")
        #self.nome_parceiro_termo_aceite_lgpd = parceiro.get("NomeParceiroTermoAceiteLGPD")
        self.importacao_contato_pliq = 0
        self.qnt_vezes_importado_para_pliq = 0
        print(self)

#         #raise ValidationError({'qty': 'Quantity must be non-negative.'})
#         from apps.lgpd.sas import sas_buscar_parceiro_por_cpf
#         parceiro = sas_buscar_parceiro_por_cpf(self.cgc_cpf)
#         if not parceiro:
#             from django.core.exceptions import ValidationError
#             raise ValidationError("Participante não localizado no FOCO")
# 
#         parceiro = parceiro[0]
# 
#         self.cod_sebrae = parceiro.get("CodSebrae")
#         self.desc_sebrae = parceiro.get("DescSebrae")
#         self.cgc_cpf = parceiro.get("CgcCpf")
#         self.cod_parceiro = parceiro.get("CodParceiro")
#         self.numero = parceiro.get("Numero")
#         self.nome_razao_social = parceiro.get("NomeRazaoSocial")
# #         self.cod_cid = parceiro.get("CodCid", 1)
# #         self.desc_cid = parceiro.get("DescCid", "1")
# #         self.cod_est = parceiro.get("CodEst", 1)
# #         self.desc_est = parceiro.get("DescEst", "1")
#         self.cod_cid = 1
#         self.desc_cid = "1"
#         self.cod_est =  1
#         self.desc_est = "1"
#         self.situacao = parceiro.get("Situacao")
#         self.deficiencia = parceiro.get("Deficiencia")
#         self.sit_cadastral = parceiro.get("sit_cadastral")
#         self.desc_sit_cadastral = parceiro.get("Desc_sit_Cadastral")
#         self.data_inclusao = parceiro.get("DataInclusao")
#         self.data_ultima_alteracao = parceiro.get("DataUltimaAlteracao")
#         self.termo_aceite_lgpd = parceiro.get("TermoAceiteLGPD")
#         self.data_inclusao_termo_aceite_lgpd = parceiro.get("DataInclusaoTermoAceiteLGPD")
#         self.cod_sebrae_termo_aceite_lgpd = parceiro.get("CodSebraeTermoAceiteLGPD")
#         self.desc_sebrae_termo_aceite_lgpd = parceiro.get("DescSebraeTermoAceiteLGPD")
#         self.cod_parceiro_termo_aceite_lgpd = parceiro.get("CodParceiroTermoAceiteLGPD")
#         self.nome_parceiro_termo_aceite_lgpd = parceiro.get("NomeParceiroTermoAceiteLGPD")
#         self.importacao_contato_pliq = 0
#         self.qnt_vezes_importado_para_pliq = 0

        super(SebraeParceiro, self).save(*args, **kwargs)

        if not self.termo_aceite_lgpd:
            pliq_cadastrar_contato(self.cgc_cpf, self.numero, self.nome_razao_social)
            self.importacao_contato_pliq = True
            self.qnt_vezes_importado_para_pliq += 1
            self.data_inclusao_importacao_pliq = datetime.now()
            super(SebraeParceiro, self).save(*args, **kwargs)

