from django.urls import path
from . import views
from app.controller import authview

urlpatterns = [
    path('', views.home, name='index'),
    path('users/', views.users, name='users'),
    path('leads/', views.leads, name='leads'),

    path('register/', authview.register, name='register'),
    path('login/', authview.loginview, name='loginview'),
    path('logout/', authview.logoutview, name='logoutview'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_leads/', views.leads_dashboard, name='dashboard_leads'),
    path('leads/marcar_atendido/<int:lead_id>/', views.marcar_atendido, name='marcar_atendido'),
    path('leads/marcar_convertido/<int:lead_id>/', views.marcar_convertido, name='marcar_convertido'),
    
    path('contratos_ativos/', views.contratos_ativos, name='contratos_ativos'),
    path('upload_contract/<int:client_id>/', views.upload_contract, name='upload_contract'),
    path('ativar_servico/<int:client_id>/', views.ativar_servico, name='ativar_servico'),

    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('contratos_ativos/', views.contratos_ativos_cliente, name='contratos_ativos_cliente'),
    path('faturas/', views.pagamento_faturas, name='pagamento_faturas'),
    path('faturas/pagar/<int:fatura_id>/', views.pagar_fatura, name='pagar_fatura'),

    path('api/total_leads/', views.total_leads, name='total_leads'),
]
