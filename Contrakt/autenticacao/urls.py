from django.urls import path
from . import views

app_name = 'autenticacao'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('forgot/', views.forgot_view, name='forgot'),
    path('login-submit/', views.login_submit, name='login_submit'),
]
