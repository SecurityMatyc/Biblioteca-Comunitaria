# Biblioteca Comunitaria MJV 📚

Proyecto academico desarrollado durante 2025 para la **Evaluacion 4 de Ingenieria de Software**.

Este sistema representa una biblioteca comunitaria ficticia orientada a la gestion de libros, usuarios y prestamos, con enfoque en una experiencia web funcional para lector, bibliotecario y administrador.

## 👥 Autores

- Matias Gajardo
- Jean Pierre Avastia
- Valentina Roldan

Trabajo realizado en conjunto como parte del proceso formativo en desarrollo de software.

## 🧩 Descripcion del proyecto

La aplicacion permite administrar los procesos principales de una biblioteca comunitaria moderna:

- Registro y gestion de usuarios con roles.
- Catalogo de libros con control de disponibilidad.
- Registro de prestamos con validaciones de negocio.
- Registro de devoluciones y calculo automatico de multas.
- Paneles diferenciados para lector, bibliotecario y administrador.

Ademas de la parte de gestion, el proyecto incorpora una interfaz web responsive con un template visual cuidado, donde quedaron funcionales:

- Inicio publico con secciones informativas.
- Seccion de servicios.
- Seccion de contacto.
- Inicio de sesion.
- Registro de cuenta.

## ✨ Caracteristicas principales

- CRUD de libros para perfil bibliotecario.
- Control estricto de disponibilidad para evitar prestamos duplicados.
- Multas automaticas por atraso (`$1000` por dia).
- Consultas por busqueda en catalogo y vistas de disponibilidad.
- Gestion administrativa de usuarios: activar/desactivar, cambio de rol y creacion de bibliotecarios.
- Validaciones robustas en registro: RUT chileno, telefono y fortaleza de contrasena.
- Dashboard con metricas de libros, prestamos y multas.

## 🛠️ Stack tecnologico

- Python 3.13
- Django 5.2.8
- Django REST Framework (instalado en el proyecto)
- HTML, CSS, JavaScript
- Bootstrap 5
- SQLite (base de datos por defecto)

## 🗂️ Modulos del sistema

- `cuentas`: autenticacion, registro, perfiles y control de roles.
- `gestion`: catalogo de libros, prestamos, devoluciones, disponibilidad y reportes.
- `biblioteca`: configuracion principal del proyecto Django.

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
- `http://127.0.0.1:8000/login/` (autenticacion)

## ☁️ Despliegue

Esta version del proyecto **no fue desplegada en AWS**.
El foco principal fue consolidar una entrega academica final, funcional y completa.

## 🎯 Contexto academico

Este repositorio conserva una entrega importante del curso para revisar decisiones de diseno, estructura y avances logrados durante la asignatura.

Proceso de trabajo considerado:

- En las primeras unidades, el trabajo fue mayoritariamente teorico.
- Antes de codificar, se desarrollaron mockups y planificacion paso a paso.
- En la Evaluacion 3 se presento una version base del sistema.
- En esta Evaluacion 4 se consolido la version final, con mejoras de interfaz, validaciones y flujo funcional completo.

## 📌 Resumen

Una base solida en Django para gestion bibliotecaria, desarrollada en equipo, con enfoque practico y buen nivel de cierre academico para servir como referencia en proyectos futuros.