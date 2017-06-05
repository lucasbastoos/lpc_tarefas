from django.http import HttpResponse
from .models import *

def index(request):
    html = """<h1>Opções</h1>
                <ul>
                    <li><a href='/user'>Usuario</a></li>
                </ul>
            """
    return HttpResponse(html)

def user(request):
    html = "<h1> Users </h1>"
    users = Usuario.objects.all()
    for user in users:
        html += ('<li>User: %s</li>' %(user.nome))
        html += ('<ul><li>E-mail: %s</li>'.format(user.mail))
        html += ('<li>Senha: %s</li>' %(user.senha))
    return HttpResponse(html)
