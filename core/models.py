from django.db import models
from django.conf import settings

# Create your models here.
class Vacina(models.Model):
    nome = models.CharField(max_length=200)
    def __str__(self):
        return self.nome

class UF(models.Model):
    nome = models.CharField(max_length=200)
    def __str__(self):
        return self.nome

class Municipio(models.Model):
    nome = models.CharField(max_length=200)
    uf = models.ForeignKey(
        UF, on_delete=models.CASCADE, null=True
    )
    def __str__(self):
        return self.nome

class Estabelecimento(models.Model):
    razaoSocial = models.CharField(max_length=200)
    nomeFantasia = models.CharField(max_length=200)
    municipio = models.ForeignKey(
        Municipio, on_delete=models.CASCADE, null=True
    )
    def __str__(self):
        return self.nomeFantasia

class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        null=True,
    )
    def __str__(self):
        return self.nome

class Profissional(models.Model):
    nome = models.CharField(max_length=200)
    estabelecimento = models.ForeignKey(
        Estabelecimento, on_delete=models.CASCADE, null=True
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        null=True,
    )
    def __str__(self):
        return self.nome

class Agenda(models.Model):
    data = models.DateField()
    fila = models.IntegerField() #número de pacientes que já entraram na fila
    fila_chamada = models.IntegerField()
    estabelecimento = models.ForeignKey(
        Estabelecimento, on_delete=models.CASCADE, null=True
    )
    def __str__(self):
        return self.estabelecimento.nomeFantasia + ' ' + self.data.strftime('%d/%m/%y')

class HorarioAgenda(models.Model): #agendamento + fila
    horario = models.TimeField(null=True, blank=True) 
    hora_chegada = models.TimeField(null=True, blank=True)
    hora_chamada = models.TimeField(null=True, blank=True)
    hora_atendimento = models.TimeField(null=True, blank=True)
    confirmacao = models.BooleanField(default=False)
    fila = models.IntegerField(default=0)
    agenda = models.ForeignKey(
        Agenda, on_delete=models.CASCADE, null=True, blank=True
    )
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, null=True, blank=True
    )
    vacina = models.ForeignKey(
        Vacina, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.agenda.data.strftime('%d/%m/%y') + ' ' + self.horario.strftime('%I:%M %p') + ' ' + self.agenda.estabelecimento.nomeFantasia

class PacienteVacina(models.Model): #cartao de vacina
    data = models.DateField()
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, null=True
    )
    vacina = models.ForeignKey(
        Vacina, on_delete=models.CASCADE, null=True
    )
    def __str__(self):
        return self.data.strftime('%d/%m/%y %I:%M %S %p') + ' ' + self.paciente.nome + ' ' + self.vacina.nome

class Estoque(models.Model):
    quantidade = models.IntegerField()
    vacina = models.ForeignKey(
        Vacina, on_delete=models.CASCADE, null=True
    )
    estabelecimento = models.ForeignKey(
        Estabelecimento, on_delete=models.CASCADE, null=True
    )
    def __str__(self):
        return self.vacina.nome + ' ' + str(self.quantidade) + ' ' + self.estabelecimento.nomeFantasia