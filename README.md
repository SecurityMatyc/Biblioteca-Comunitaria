# Biblioteca Comunitaria MJV 📚

Proyecto académico desarrollado durante 2025 para la **Evaluación 4 de Ingeniería de Software**.

Este sistema representa una biblioteca comunitaria ficticia orientada a la gestión de libros, usuarios y préstamos, con enfoque en una experiencia web funcional para lector, bibliotecario y administrador.

Actualmente, el proyecto se encuentra **completamente funcional**, incluyendo inicio, servicios, contacto, inicio de sesión y registro de cuentas.

## 👥 Autores

- Matias Gajardo
- Jean Pierre Avastia
- Valentina Roldan

Trabajo realizado en conjunto como parte del proceso formativo en desarrollo de software.

## 🧩 Descripción del proyecto

La aplicación permite administrar los procesos principales de una biblioteca comunitaria moderna:

- Registro y gestión de usuarios con roles.
- Catálogo de libros con control de disponibilidad.
- Registro de préstamos con validaciones de negocio.
- Registro de devoluciones y cálculo automático de multas.
- Paneles diferenciados para lector, bibliotecario y administrador.

Además de la parte de gestión, el proyecto incorpora una interfaz web responsive con un template visual cuidado, donde quedaron funcionales:

- Inicio público con secciones informativas.
- Sección de servicios.
- Sección de contacto.
- Inicio de sesión.
- Registro de cuenta.

## ✨ Características principales

- CRUD de libros para perfil bibliotecario.
- Control estricto de disponibilidad para evitar prestamos duplicados.
- Multas automáticas por atraso (`$1000` por día).
- Consultas por búsqueda en catálogo y vistas de disponibilidad.
- Gestión administrativa de usuarios: activar/desactivar, cambio de rol y creación de bibliotecarios.
- Validaciones robustas en registro: RUT chileno, teléfono y fortaleza de contraseña.
- Dashboard con métricas de libros, préstamos y multas.

## 🛠️ Stack tecnológico

- Python 3.13
- Django 5.2.8
- Django REST Framework (instalado en el proyecto)
- HTML, CSS, JavaScript
- Bootstrap 5
- SQLite (base de datos por defecto)

## 🗂️ Modulos del sistema

- `cuentas`: autenticación, registro, perfiles y control de roles.
- `gestion`: catálogo de libros, préstamos, devoluciones, disponibilidad y reportes.
- `biblioteca`: configuración principal del proyecto Django.

## 🚀 Puesta en marcha local

1. Clonar el repositorio.
2. Entrar a la carpeta del proyecto.
3. Crear y activar entorno virtual.
4. Instalar dependencias.
5. Aplicar migraciones.
6. Iniciar servidor.

Comandos sugeridos en Windows PowerShell:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abrir en navegador:

- `http://127.0.0.1:8000/` (sitio principal)
- `http://127.0.0.1:8000/admin/` (panel Django Admin)
- `http://127.0.0.1:8000/login/` (autenticación)

## ☁️ Despliegue

Esta versión del proyecto **no fue desplegada en AWS**.
El foco principal fue consolidar una entrega académica final, funcional y completa.

## 🎯 Contexto académico

Este repositorio conserva una entrega importante del curso para revisar decisiones de diseño, estructura y avances logrados durante la asignatura.

Proceso de trabajo considerado:

- En las primeras unidades, el trabajo fue mayoritariamente teórico.
- Antes de codificar, se desarrollaron mockups y planificación paso a paso.
- En la Evaluación 3 se presentó una versión base del sistema.
- En esta Evaluación 4 se consolidó la versión final, con mejoras de interfaz, validaciones y flujo funcional completo.

## 📌 Resumen

Una base sólida en Django para gestión bibliotecaria, desarrollada en equipo, con enfoque práctico y buen nivel de cierre académico para servir como referencia en proyectos futuros.