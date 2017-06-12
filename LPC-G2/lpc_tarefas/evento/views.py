from django.http import HttpResponse
from .models import *

def listaUsuarios(request):
    html = "<h1>Lista de Usuarios</h1>"
    listaPessoa = Usuario.objects.all()
    for usuario in listaPessoa:
        html += '<li><strong>{}</strong></li>'.format(usuario.nome)
        html += '<ul><li>Email: {}</li></ul>'.format(usuario.email)
        html += '<ul><li>Password: {}</li></ul>'.format(usuario.password)
    return HttpResponse(html)
