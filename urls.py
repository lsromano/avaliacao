from django.contrib import admin
from django.urls import path, include
from autenticacao.views import index, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('contratos/', include('contratos.urls')),
    path('autenticacao/', include('autenticacao.urls')),
]