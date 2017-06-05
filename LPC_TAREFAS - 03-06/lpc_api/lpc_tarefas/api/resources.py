from tastypie.resources import ModelResource
from tastypie import fields, utils
from lpc_tarefas.models import *
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class UsuarioResource(ModelResource):
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Você não tem permissão !")

    def obj_create(self, bundle, **kwargs):
        users = Usuario.objects.all()
        if (Usuario.objects.filter(Nome= bundle.data['Nome']) or Usuario.objects.filter(Email = bundle.data['Email'])):
            raise Unauthorized ("Usuario já cadastrado")
        else:
            user = Usuario()
            user.Nome = bundle.data['Nome']
            user.Password = bundle.data['Password']
            user.Email = bundle.data['Email']
            user.save()
            bundle.obj = user
            return bundle

    class Meta:
        resource_name = "user"
        queryset = Usuario.objects.all()
        allowed_methods = ['get','post', 'delete', 'put']
        authorization = Authorization()
        filtering = {"nome":('exact')}


class ProjetoResource(ModelResource):
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Você não tem permissão !")

    def obj_create(self, bundle, **kwargs):
        nome = bundle.data['Nome']
        if not (Projeto.objects.filter(Nome = nome)):
            projeto = Projeto()
            projeto.Nome = nome;
            projeto.save()
            bundle.obj = projeto
            return bundle

        else:
            raise Unauthorized("Nome já cadastrado !")

    class Meta:
        resource_name = "projeto"
        queryset = Projeto.objects.all()
        allowed_methods = ['get','post', 'delete', 'put']
        authorization = Authorization()
        filtering = {"nome":('exact', 'startswith', 'contains', 'endswith')}

class ProjetoUsuarioResource(ModelResource):
    usuario = fields.ToOneField(UsuarioResource, "usuario")
    projeto = fields.ToOneField(ProjetoResource, "projeto")

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Você não tem permissão !")

    class Meta:
        resource_name = "projetoUser"
        queryset = ProjetoUsuario.objects.all()
        allowed_methods = ['get','post', 'delete', 'put']
        authorization = Authorization()
        filtering = {"nome":('exact', 'startswith', 'contains', 'endswith')}



class TarefaResource(ModelResource):

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Você não tem permissão !")

    def obj_create(self, bundle, **kwargs):
        projeto = bundle.data['projeto'].split("/")[4]
        if not (Tarefa.objects.filter(projeto = projeto)):
            tarefa = Tarefa()
            tarefa.Nome = bundle.data['nome']
            tarefa.usuario = Usuario.objects.get(pk=bundle.data['usuario'].split("/")[4])
            tarefa.projeto = Projeto.objects.get(pk = projeto)
            tarefa.save()
            bundle.obj = tarefa
            return bundle
        else:
            raise Unauthorized ("Não é permitido que uma tarefa seja associada a mais de um projeto !")

    def obj_update(self, bundle, **kwargs):
        nome = bundle.data["nome"]
        p_id = bundle.data['projeto'].split("/")[4]
        projeto = Projeto.objects.get(pk = p_id)
        p_user = bundle.data['usuario'].split("/")[4]
        user = Usuario.objects.get(pk = p_user)
        tarefas = Tarefa.objects.filter(projeto = projeto)
        for tarefa in tarefas:
            if (tarefa.usuario == user):
                tarefa.nome = nome
                tarefa.usuario = user
                tarefa.projeto = projeto
                tarefa.save()
                bundle.obj = tarefa
                return bundle
        raise Unauthorized("Usuario incorreto !")


    projeto = fields.ToOneField(ProjetoResource, "projeto")
    class Meta:
        resource_name = "tarefa"
        queryset = Tarefa.objects.all()
        allowed_methods = ['get','post', 'delete', 'put']
        authorization = Authorization()
        filtering = {"nome":('exact', 'startswith', 'contains', 'endswith')}
