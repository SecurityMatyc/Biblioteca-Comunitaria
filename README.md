# Sistema de Gestión para Biblioteca Comunitaria

Sistema web desarrollado en Django para la gestión integral de una biblioteca comunitaria, permitiendo el control de préstamos, devoluciones, usuarios y catálogo de libros.

## 📋 Características

- **Gestión de Libros**: Catálogo completo con información de disponibilidad
- **Sistema de Préstamos**: Control de préstamos y devoluciones
- **Gestión de Usuarios**: Diferentes roles (Lector, Bibliotecario, Administrador)
- **Sistema de Multas**: Cálculo automático por retrasos
- **Panel de Control**: Dashboard intuitivo para bibliotecarios

## 🏗️ Estructura del Proyecto

```
biblioteca-comunitaria/
├── biblioteca/          # Configuración principal del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── static/         # Archivos estáticos (CSS, JS, imágenes)
├── gestion/            # App principal - gestión de libros y préstamos
│   ├── models.py       # Modelos: Libro, Prestamo
│   ├── views.py        # Vistas de gestión
│   ├── urls.py
│   ├── templates/      # Templates de gestión
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── disponibilidad_libros.html
│   │   ├── gestionar_libros.html
│   │   ├── registrar_prestamo.html
│   │   └── registrar_devolucion.html
│   └── migrations/
├── cuentas/            # App de gestión de usuarios y autenticación
│   ├── models.py       # Modelo: PerfilUsuario
│   ├── views.py        # Login, Registro, Paneles
│   ├── urls.py
│   ├── templates/      # Templates de usuarios
│   │   ├── login.html
│   │   ├── registro.html
│   │   ├── panel_usuario.html
│   │   └── panel_bibliotecario.html
│   └── migrations/
├── db.sqlite3          # Base de datos SQLite
├── manage.py           # Script de gestión de Django
└── requirements.txt    # Dependencias del proyecto
```

Ver [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md) para documentación detallada.

## 🚀 Instalación

1. **Clonar el repositorio**
```bash
git clone [url-del-repositorio]
cd Biblioteca-Comunitaria
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor**
```bash
python manage.py runserver
```

El servidor estará disponible en `http://127.0.0.1:8000/`

## 🔧 Tecnologías Utilizadas

- **Django 5.2.8**: Framework web principal
- **Django REST Framework**: Para la API REST
- **SQLite**: Base de datos
- **HTML/CSS/JavaScript**: Frontend
- **Bootstrap**: Framework CSS (opcional)

## 👥 Roles de Usuario

- **Lector**: Puede ver el catálogo y sus préstamos activos
- **Bibliotecario**: Gestiona préstamos, devoluciones y libros
- **Administrador**: Acceso completo al sistema

## 📝 Uso

1. Acceder al panel de administración: `http://127.0.0.1:8000/admin/`
2. Iniciar sesión con las credenciales del superusuario
3. Crear usuarios y asignar roles
4. Gestionar el catálogo de libros
5. Registrar préstamos y devoluciones

## 🔄 Aplicaciones

### `gestion`
**Responsabilidad:** Gestión de libros, préstamos y devoluciones

**Funcionalidades:**
- Catálogo de libros con búsqueda
- Sistema de préstamos con validaciones
- Registro de devoluciones con cálculo de multas
- CRUD de libros para bibliotecarios
- Dashboard principal

**Templates:** index, home, dashboard, disponibilidad_libros, gestionar_libros, registrar_prestamo, registrar_devolucion

### `cuentas`
**Responsabilidad:** Autenticación, usuarios y perfiles

**Funcionalidades:**
- Sistema de login/registro
- Gestión de perfiles de usuario
- Roles: Lector, Bibliotecario, Administrador
- Panel personal del usuario
- Panel de estadísticas para bibliotecarios

**Templates:** login, registro, panel_usuario, panel_bibliotecario

## 📄 Licencia

Este proyecto es de uso académico/educativo.

## ✨ Autor

Desarrollado como proyecto de evaluación para Sistema de Gestión de Biblioteca Comunitaria.
