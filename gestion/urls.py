from django.urls import path
from . import views

urlpatterns = [
    # Vistas públicas y dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Funcionalidades de préstamos (Lectores)
    path('prestamo/', views.registrar_prestamo, name='registrar_prestamo'),
    path('devolucion/', views.registrar_devolucion, name='registrar_devolucion'),
    path('disponibilidad/', views.disponibilidad_libros, name='disponibilidad_libros'),
    
    # Gestión de libros (Bibliotecarios)
    path('gestionar-libros/', views.gestionar_libros, name='gestionar_libros'),
    path("prestamos/activos/", views.prestamos_activos, name="prestamos_activos"),

]