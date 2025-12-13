
from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Paneles de usuario
    path('panel-bibliotecario/', views.panel_bibliotecario, name='panel_bibliotecario'),
    path('panel-usuario/', views.panel_usuario, name='panel_usuario'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]