from django.db import models
from autenticacao.models import CustomUser
import datetime


class Contrato(models.Model) :

    # para definir se o contrato esta ativo ou inativo
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    # atributos
    # on_delete=models.CASCADE) se o usuario for excluido, todos os contratos relacionado a ele tambem serao.
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contract_title = models.CharField(max_length=255)
    involved_parties = models.TextField()
    validity_start_date = models.DateField()
    validity_end_date = models.DateField()
    specific_clauses = models.TextField()
    description = models.TextField()

    ultima_atualizacao = models.DateTimeField(auto_now=True)
    # se usar models.DateTimeField(auto_now=True) no creation_date, ele vai mudar sempre que atualizar o contrato.
    creation_date = models.DateTimeField(default=datetime.datetime.now) #  campo preenchido com a data e hora

    # Campo para o anexo
    attachment = models.FileField(upload_to='attachments/', default='temp.pdf')

    def registrar_alteracao(self, usuario, alteracoes) :
        HistoricoAlteracoes.objects.create(contrato=self, usuario=usuario, alteracoes=alteracoes)

    def __str__(self) : # retorna o título do contrato
        return self.contract_title


class HistoricoAlteracoes(models.Model) :
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now=True)
    alteracoes = models.TextField()


class Alerta(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    data_alerta = models.DateField()
    mensagem = models.TextField(blank=True) # inativo

    def __str__(self):
        return f"Alerta de Prazo: {self.contrato.contract_title}"
