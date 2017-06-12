from tastypie.resources import ModelResource
from tastypie import fields, utils
from evento.models import *
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from django.http.request import *

class UsuarioResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        #authorization = Authorization()
        #authentication = ApiKeyAuthentication() # pede usuário e token
        authentication = BasicAuthentication()
        excludes = ['password', 'is_active', 'last_name', 'first_name', 'is_staff', 'is_superuser', 'last_login']



    def obj_delete_list(self, **kwargs):
        raise Unauthorized('Você não pode apagar a lista.')


    def obj_create(self, bundle, **kwargs):
        try:
            nome = bundle.data["nome"]
            email = bundle.data["email"]
            senha = bundle.data["password"]
            user = User.objects.create_user(nome, email, senha, is_superuser = True, is_staff = True)
            print ("Cadastrado !")
        except Exception as e:
            raise Unauthorized("Usuario já cadastrado !")


class ProjetoResource(ModelResource):
    class Meta:
        queryset = Projeto.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()

    def obj_delete_list(self, **kwargs):
        raise Unauthorized('Você não pode apagar a lista.')


class ProjetoUsuarioResource(ModelResource):
    class Meta:
        queryset = ProjetoUsuario.objects.all()
        resource_name = 'projetousuario'
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()

    def obj_delete_list(self, varBundle, **kwargs):
        raise Unauthorized('Você não pode apagar a lista.')


class TarefaResource(ModelResource):
    class Meta:
        queryset = Tarefa.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authentication = BasicAuthentication()

    def obj_delete_list(self, varBundle, **kwargs):
        raise Unauthorized('Você não pode apagar a lista.')

    def obj_create(self, bundle, **kwargs):
        data = bundle.data
        id = data["usuario"].split("/")[4]
        user = User.objects.get(pk=id)
        projeto = Projeto.objects.get(pk = data["projeto"].split("/")[4])
        if not (Tarefa.objects.filter(nome = bundle.data['nome'])):
            tarefa = Tarefa()
            tarefa.nome = bundle.data['nome']
            tarefa.usuario = user
            tarefa.projeto = bundle.data['projeto']
            tarefa.save()
            bundle.obj = tarefa
            return bundle
        else:
            raise Unauthorized('Já existe essa tarefa em um projeto')

    def obj_update(self, bundle, **kwargs):
        tarefa = Tarefa.objects.get(pk = int(kwargs['pk']))
        nomet = bundle.data['nome']
        usuario = bundle.data['usuario'].split('/')
        projeto = bundle.data['projeto'].split('/')
        id = usuario[4] #14
        nome = tarefa.usuario
        dono = User.objects.filter(id = id)
        projeto = Projeto.objects.get(pk=projeto[4])
        logado = bundle.request.user
        if (logado == nome):
            tarefa.nome = str(nomet)
            tarefa.usuario = logado
            tarefa.projeto = projeto
            tarefa.save()

        else:
            raise Unauthorized("Você não tem permissão para alterar esta tarefa !")


    def obj_delete(self, bundle, **kwargs):
        tarefa = Tarefa.objects.get(pk = int(kwargs['pk']))
        print (tarefa)
        user = tarefa.usuario
        print (user)
        if (user == bundle.request.user):
            print ("foi menos ruim")


        else:
            print ("deu nao")





















    usuario = fields.ToOneField(UsuarioResource, 'usuario')
    projeto = fields.ToOneField(ProjetoResource, 'projeto')
