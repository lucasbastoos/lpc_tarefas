from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User)
    def __str__(self):
        return '{}:{}'.format(self.nome, self.email)


class Projeto(models.Model):
    nome = models.CharField('nome', max_length=200)

    def __str__(self):
        return '{}'.format(self.nome)


class ProjetoUsuario(models.Model):
    usuario = models.ForeignKey('auth.User')
    projeto = models.ForeignKey('Projeto')

    def __str__(self):
        return '{}'.format(self.usuario)


class Tarefa(models.Model):
    nome = models.CharField('nome', max_length=100)
    usuario = models.ForeignKey("auth.User")
    projeto = models.ForeignKey('Projeto')
    dataEHoraDeInicio = models.DateTimeField('dataEHoraDeInicio', default=timezone.now)

    def __str__(self):
        return '{}'.format(self.nome)
