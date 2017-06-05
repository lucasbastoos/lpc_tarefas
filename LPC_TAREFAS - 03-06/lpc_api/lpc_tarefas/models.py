from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nome  = models.CharField(name = "Nome", max_length = 200);
    mail = models.CharField(name = "Email", max_length = 200);
    senha = models.CharField(name ="Password", max_length = 200)


    def __str__(self):
        return "Nome: %s \n Pass: %s \n E-Mail: %s" %(self.Nome, self.Password , self.Email)


class Projeto(models.Model):
    nome = models.CharField(name = "Nome", max_length = 200);

    def __str__(self):
        return "{}".format(self.Nome)

class ProjetoUsuario(models.Model):
    usuario = models.ForeignKey(Usuario)
    projeto = models.ForeignKey(Projeto)

    def __str__(self):
        return "{}:{}".format(self.usuario, self.projeto)

class Tarefa(models.Model):
    nome = models.CharField(name = "nome", max_length = 200)
    dataEHoraDeInicio = models.DateTimeField(name = "Data e Hora de Inicio", default = timezone.now)
    usuario = models.ForeignKey(Usuario)
    projeto = models.ForeignKey(Projeto)

    def __str__(self):
        return "Nome: {} \nUsuario:[{}] \nProjeto: {}".format(self.nome, self.usuario, self.projeto)
