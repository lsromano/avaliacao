from . import views
from django.urls import path
from contratos.views import ContractDeleteView
from .views import logout_view, contract_update

app_name = 'contratos'

urlpatterns = [

    path('logout/', logout_view, name='logout'),
    path('', views.contract_list, name='contract_list'),
    path('form/', views.contract_form, name='contract_form'),
    path('criar-alerta/', views.criar_alerta, name='criar_alerta'),
    path('contratos/<int:contract_id>/detalhes/', views.contract_information, name='contract_information'),
    path('<int:pk>/delete/', ContractDeleteView.as_view(), name='contract_delete'),
    path('contract/update/<int:contrato_id>/', contract_update, name='contract_update'),
    path('historical-changes/<int:contract_id>/', views.historical_changes, name='historical_changes'),
    path('contract/attachment/<int:contrato_id>/', views.download_attachment, name='download_attachment'),



]
