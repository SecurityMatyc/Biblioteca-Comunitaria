# Sistema de Gestión para Biblioteca Comunitaria

Sistema web desarrollado en Django para la gestión integral de una biblioteca comunitaria, permitiendo el control de préstamos, devoluciones, usuarios y catálogo de libros.

## Requisitos

- Python 3.10 o superior
- pip
- (Opcional) Entorno virtual (recomendado)

## Instalación y configuración

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/Biblioteca-Comunitaria.git
   cd Biblioteca-Comunitaria
   ```

2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv env
   # En Windows:
   env\Scripts\activate
   # En Linux/Mac:
   source env/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

- Las contraseñas de usuarios se almacenan de forma segura usando el sistema de Django (hash y sal).
- No compartas tu `SECRET_KEY` ni credenciales de superusuario.

## Migraciones y base de datos

1. **Aplica las migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Crea un superusuario (admin):**
   ```bash
   python manage.py createsuperuser
   ```

## Carga de datos de ejemplo (opcional)

Si deseas poblar la base de datos con datos de ejemplo, puedes crear fixtures o usar la interfaz de administración de Django (`/admin`).

## Ejecución del servidor

1. **Inicia el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

2. Accede a la aplicación en [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

3. Para detener el servidor, presiona `Ctrl+C` en la terminal.

## Seguridad y buenas prácticas

- El sistema implementa validación de entrada, control de acceso por roles, manejo seguro de credenciales y errores personalizados.
- Para producción, asegúrate de:
  - Usar `DEBUG=False`.
  - Configurar correctamente `ALLOWED_HOSTS`.
  - Proteger tu `SECRET_KEY` y credenciales.
  - Usar HTTPS.
- Para más detalles, revisa el informe técnico adjunto.

## Estructura del proyecto

- `biblioteca/` – Configuración principal de Django
- `cuentas/` – Gestión de usuarios y autenticación
- `gestion/` – Funcionalidad principal de la biblioteca
- `requirements.txt` – Dependencias del proyecto