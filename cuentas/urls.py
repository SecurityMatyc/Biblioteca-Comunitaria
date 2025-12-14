
from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path("dashboard/", views.dashboard, name="dashboard"),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    
    # Paneles de usuario
    path('panel-bibliotecario/', views.panel_bibliotecario, name='panel_bibliotecario'),
    path("multas/", views.ver_multas, name="ver_multas"),
    path('panel-usuario/', views.panel_usuario, name='panel_usuario'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),

    path("admin-panel/usuarios/", views.admin_usuarios, name="admin_usuarios"),
    path("admin-panel/usuarios/toggle/<int:user_id>/", views.admin_toggle_usuario, name="admin_toggle_usuario"),
    path("admin-panel/crear-bibliotecario/", views.admin_crear_bibliotecario, name="admin_crear_bibliotecario"),
    path("admin-panel/usuarios/rol/<int:user_id>/<str:rol>/", views.admin_cambiar_rol, name="admin_cambiar_rol"),
    path("panel-admin/", views.panel_admin, name="panel_admin"),

]