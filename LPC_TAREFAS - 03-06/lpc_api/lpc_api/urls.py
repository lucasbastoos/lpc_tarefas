''''''
from django.conf.urls import url, include
from tastypie.api import Api
from django.contrib import admin
from lpc_tarefas.api.resources import *

from lpc_tarefas.views import *

v1_api = Api(api_name='v1')
v1_api.register(UsuarioResource())
v1_api.register(ProjetoResource())
v1_api.register(ProjetoUsuarioResource())
v1_api.register(TarefaResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^user/', user, name='user'),
    url(r'^api/', include(v1_api.urls)),
]
