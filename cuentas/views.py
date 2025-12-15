from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from cuentas.restringir import login_exigido
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from .models import PerfilUsuario
from django.shortcuts import render, redirect, get_object_or_404
from .restringir import role_required
from .forms import CrearBibliotecarioForm
from decimal import Decimal
from django.db.models import Q
from django.shortcuts import render
from gestion.models import Libro, Prestamo
import re


@login_exigido
@login_exigido
def dashboard(request):
    # Seguridad: si no tiene perfil
    if not hasattr(request.user, "perfil"):
        return redirect("panel_usuario")

    rol = request.user.perfil.rol

    if rol == "administrador":
        return redirect("panel_admin")

    if rol == "bibliotecario":
        return redirect("panel_bibliotecario")

    return redirect("panel_usuario")



@login_exigido
def dashboard_admin(request):
    if request.user.perfil.rol != "administrador":
        messages.error(request, "No tienes permisos para acceder a este panel.")
        return redirect("dashboard")

    hoy = timezone.now().date()

    total_libros = Libro.objects.count()
    total_usuarios = User.objects.count()
    prestamos_vencidos = Prestamo.objects.filter(
        fecha_devolucion_real__isnull=True,
        fecha_devolucion_esperada__lt=hoy
    ).count()

    total_multas = sum(
        p.multa for p in Prestamo.objects.filter(multa__gt=0)
    )

    context = {
        "total_libros": total_libros,
        "total_usuarios": total_usuarios,
        "prestamos_vencidos": prestamos_vencidos,
        "total_multas": total_multas,
    }

    return render(request, "dashboard_admin.html", context)


@role_required("administrador")
def admin_usuarios(request):
    usuarios = User.objects.select_related("perfil").all().order_by("username")
    return render(request, "admin/usuarios.html", {"usuarios": usuarios})

@role_required("administrador")
def admin_toggle_usuario(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if u == request.user:
        messages.error(request, "No puedes desactivarte a ti mismo.")
        return redirect("admin_usuarios")
    u.is_active = not u.is_active
    u.save()
    messages.success(request, f"Usuario '{u.username}' actualizado correctamente.")
    return redirect("admin_usuarios")

@role_required("administrador")
def admin_crear_bibliotecario(request):
    if request.method == "POST":
        form = CrearBibliotecarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bibliotecario creado correctamente.")
            return redirect("admin_usuarios")
    else:
        form = CrearBibliotecarioForm()
    return render(request, "admin/crear_bibliotecario.html", {"form": form})

@role_required("administrador")
def admin_cambiar_rol(request, user_id, rol):
    u = get_object_or_404(User, id=user_id)
    # No permitir que el admin se cambie su propio rol
    if u == request.user:
        messages.error(request, "No puedes cambiarte tu propio rol.")
        return redirect("admin_usuarios")

    if rol not in ["lector", "bibliotecario"]:
        messages.error(request, "Rol inválido.")
        return redirect("admin_usuarios")

    # Crear perfil si no existe (forma segura)
    PerfilUsuario.objects.get_or_create(
        usuario=u,
        defaults={
            "rol": "lector",
            "rut": f"SINRUT-{u.id}",
            "direccion": "",
            "telefono": "",
        }
    )

    # Cambiar rol
    u.perfil.rol = rol
    u.perfil.save()

    messages.success(request, f"Rol de '{u.username}' cambiado a {rol}.")
    return redirect("admin_usuarios")


def validar_rut(rut):
    """Valida RUT chileno con dígito verificador"""
    # Limpiar RUT (quitar puntos y guión)
    rut = rut.replace(".", "").replace("-", "").upper()
    
    # Verificar largo
    if len(rut) < 2:
        return False
    
    # Separar número y dígito verificador
    rut_numero = rut[:-1]
    digito_verificador = rut[-1]
    
    # Verificar que el número sea válido
    if not rut_numero.isdigit():
        return False
    
    # Calcular dígito verificador esperado (algoritmo módulo 11)
    suma = 0
    multiplicador = 2
    
    for digito in reversed(rut_numero):
        suma += int(digito) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    
    return digito_verificador == dv_calculado


def validar_contrasena(password):
    """Valida que la contraseña sea segura"""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "Debe contener al menos una mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "Debe contener al menos una minúscula"
    
    if not re.search(r'[0-9]', password):
        return False, "Debe contener al menos un número"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Debe contener al menos un carácter especial (!@#$%^&*)"
    
    return True, "Contraseña válida"


def validar_telefono(telefono):
    """Valida teléfono chileno (9 dígitos)"""
    telefono_limpio = re.sub(r'\D', '', telefono)
    return len(telefono_limpio) == 9 and telefono_limpio.isdigit()

def login_view(request):
    """Vista de Login"""
    if request.method == "POST":
        email_or_username = request.POST.get("username")  # Puede ser email o username
        password = request.POST.get("password")

        # Intentar encontrar usuario por email primero
        user_obj = User.objects.filter(email=email_or_username).first()
        
        if user_obj:
            # Si encontró por email, autenticar con el username de ese usuario
            user = authenticate(request, username=user_obj.username, password=password)
        else:
            # Si no existe el email, intentar por username directamente
            user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Correo o contraseña incorrectos")
            return render(request, "login.html")

    return render(request, "login.html")


def registro_view(request):
    """Vista de Registro de Nuevos Usuarios (Lectores)"""
    if request.method == "POST":
        # Datos del usuario
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        
        # Datos del perfil
        rut = request.POST.get("rut")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        
        # VALIDACIÓN 1: Nombres y apellidos
        if len(first_name) < 2:
            messages.error(request, "El nombre debe tener al menos 2 caracteres")
            return render(request, "registro.html")
        
        if len(last_name) < 2:
            messages.error(request, "El apellido debe tener al menos 2 caracteres")
            return render(request, "registro.html")
        
        # VALIDACIÓN 2: Email
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return render(request, "registro.html")
        
        # Generar username desde email (automático)
        username = email.split('@')[0].replace('.', '_')
        contador = 1
        username_original = username
        while User.objects.filter(username=username).exists():
            username = f"{username_original}{contador}"
            contador += 1
        
        # VALIDACIÓN 3: Contraseñas coinciden
        if password != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "registro.html")
        
        # VALIDACIÓN 4: Contraseña segura
        es_valida, mensaje = validar_contrasena(password)
        if not es_valida:
            messages.error(request, f"Contraseña insegura: {mensaje}")
            return render(request, "registro.html")
        
        # VALIDACIÓN 5: RUT chileno
        if not validar_rut(rut):
            messages.error(request, "El RUT ingresado no es válido")
            return render(request, "registro.html")
        
        # Limpiar RUT para guardarlo sin puntos ni guión
        rut_limpio = rut.replace(".", "").replace("-", "").upper()
        
        if PerfilUsuario.objects.filter(rut=rut_limpio).exists():
            messages.error(request, "El RUT ya está registrado")
            return render(request, "registro.html")
        
        # VALIDACIÓN 6: Teléfono
        if not validar_telefono(telefono):
            messages.error(request, "El teléfono debe tener 9 dígitos")
            return render(request, "registro.html")
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            
            # Crear perfil con rol "lector" por defecto
            PerfilUsuario.objects.create(
                usuario=user,
                rut=rut_limpio,
                direccion=direccion,
                telefono=telefono,
                rol='lector'
            )
            
            messages.success(request, f"Cuenta creada exitosamente. Ya puedes iniciar sesión con tu correo: {email}")
            return redirect("login")
            
        except Exception as e:
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
            return render(request, "registro.html")
    
    return render(request, "registro.html")


def logout_view(request):
    """Vista de Logout"""
    logout(request)
    messages.success(request, "Sesión cerrada exitosamente")
    return redirect("login")


@login_exigido
def editar_perfil(request):
    """Permite al usuario editar su perfil, username y contraseña"""
    if request.method == "POST":
        accion = request.POST.get("accion")
        password_actual = request.POST.get("password_actual")
        
        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            messages.error(request, "La contraseña actual es incorrecta")
            return redirect("panel_usuario")
        
        # ACCIÓN 1: Editar datos personales
        if accion == "datos":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            telefono = request.POST.get("telefono")
            direccion = request.POST.get("direccion")
            
            # Validar nombres
            if len(first_name) < 2 or len(last_name) < 2:
                messages.error(request, "Nombre y apellido deben tener al menos 2 caracteres")
                return redirect("panel_usuario")
            
            # Validar email único
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, "El correo electrónico ya está registrado por otro usuario")
                return redirect("panel_usuario")
            
            # Validar teléfono
            if not validar_telefono(telefono):
                messages.error(request, "El teléfono debe tener 9 dígitos")
                return redirect("panel_usuario")
            
            # Actualizar usuario
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            
            # Actualizar perfil
            perfil = request.user.perfil
            perfil.telefono = telefono
            perfil.direccion = direccion
            perfil.save()
            
            messages.success(request, "Datos personales actualizados correctamente")
            return redirect("panel_usuario")
        
        # ACCIÓN 2: Cambiar username
        elif accion == "username":
            nuevo_username = request.POST.get("nuevo_username")
            
            # Validar que el username sea válido
            if len(nuevo_username) < 3:
                messages.error(request, "El nombre de usuario debe tener al menos 3 caracteres")
                return redirect("panel_usuario")
            
            if not re.match(r'^[a-zA-Z0-9_]+$', nuevo_username):
                messages.error(request, "El nombre de usuario solo puede contener letras, números y guión bajo")
                return redirect("panel_usuario")
            
            # Validar que no exista
            if User.objects.filter(username=nuevo_username).exclude(id=request.user.id).exists():
                messages.error(request, "El nombre de usuario ya está en uso")
                return redirect("panel_usuario")
            
            # Actualizar
            request.user.username = nuevo_username
            request.user.save()
            
            messages.success(request, f"Nombre de usuario cambiado a: {nuevo_username}")
            return redirect("panel_usuario")
        
        # ACCIÓN 3: Cambiar contraseña
        elif accion == "password":
            nueva_password = request.POST.get("nueva_password")
            confirmar_password = request.POST.get("confirmar_password")
            
            # Validar que coincidan
            if nueva_password != confirmar_password:
                messages.error(request, "Las contraseñas no coinciden")
                return redirect("panel_usuario")
            
            # Validar seguridad de la contraseña
            es_valida, mensaje = validar_contrasena(nueva_password)
            if not es_valida:
                messages.error(request, f"Contraseña insegura: {mensaje}")
                return redirect("panel_usuario")
            
            # Cambiar contraseña
            request.user.set_password(nueva_password)
            request.user.save()
            
            # Re-autenticar para mantener la sesión
            login(request, request.user)
            
            messages.success(request, "Contraseña cambiada correctamente")
            return redirect("panel_usuario")
    
    return redirect("panel_usuario")


# ==================== PANEL DE BIBLIOTECARIO ====================

@login_exigido
def panel_bibliotecario(request):
    """
    Panel exclusivo para bibliotecarios y administradores
    Muestra estadísticas y opciones de gestión del sistema
    """
    # Verificar que el usuario es bibliotecario o administrador
    if not hasattr(request.user, 'perfil') or request.user.perfil.rol not in ['bibliotecario', 'administrador']:
        raise PermissionDenied
    
    # Importar modelos de gestion
    from gestion.models import Libro, Prestamo
    
    # Estadísticas generales
    total_libros = Libro.objects.count()
    libros_por_genero = Libro.objects.values('genero').annotate(total=Count('genero')).order_by('-total')
    prestamos_activos = Prestamo.objects.filter(fecha_devolucion_real__isnull=True).count()
    prestamos_vencidos = Prestamo.objects.filter(
        fecha_devolucion_real__isnull=True,
        fecha_devolucion_esperada__lt=timezone.now().date()
    ).count()
    
    context = {
        'total_libros': total_libros,
        'libros_por_genero': libros_por_genero,
        'prestamos_activos': prestamos_activos,
        'prestamos_vencidos': prestamos_vencidos,
    }
    return render(request, 'panel_bibliotecario.html', context)


@login_exigido
def ver_multas(request):
    # Solo bibliotecario/admin
    if not hasattr(request.user, "perfil") or request.user.perfil.rol not in ["bibliotecario", "administrador"]:
        raise PermissionDenied

    from gestion.models import Prestamo

    hoy = timezone.now().date()
    multa_por_dia = Decimal("1000.00")

    # 1) Préstamos vencidos (activos, no devueltos)
    vencidos = Prestamo.objects.filter(
        fecha_devolucion_real__isnull=True,
        fecha_devolucion_esperada__lt=hoy
    ).select_related("usuario", "libro").order_by("fecha_devolucion_esperada")

    # calcular multa estimada al día
    for p in vencidos:
        dias_atraso = (hoy - p.fecha_devolucion_esperada).days
        p.dias_atraso = dias_atraso
        p.multa_estimada = multa_por_dia * dias_atraso

    # 2) Multas registradas (ya devueltos y multa > 0)
    multas_registradas = Prestamo.objects.filter(
        fecha_devolucion_real__isnull=False,
        multa__gt=0
    ).select_related("usuario", "libro").order_by("-fecha_devolucion_real")[:50]

    total_estimado_vencidos = sum((p.multa_estimada for p in vencidos), Decimal("0.00"))
    total_multas_registradas = sum((p.multa for p in multas_registradas), Decimal("0.00"))

    context = {
        "hoy": hoy,
        "vencidos": vencidos,
        "multas_registradas": multas_registradas,
        "total_estimado_vencidos": total_estimado_vencidos,
        "total_multas_registradas": total_multas_registradas,
    }
    return render(request, "ver_multas.html", context)


# ==================== PANEL DE USUARIO ====================

@login_exigido
def panel_usuario(request):
    """
    Panel personal del usuario (lector)
    Muestra su información y préstamos activos
    """
    from gestion.models import Prestamo
    
    # Obtener perfil del usuario
    perfil = None
    if hasattr(request.user, 'perfil'):
        perfil = request.user.perfil
    
    # Préstamos activos del usuario
    mis_prestamos = Prestamo.objects.filter(
        usuario=request.user,
        fecha_devolucion_real__isnull=True
    ).select_related('libro').order_by('fecha_devolucion_esperada')
    
    # Calcular días restantes para cada préstamo
    fecha_actual = timezone.now().date()
    for prestamo in mis_prestamos:
        dias_restantes = (prestamo.fecha_devolucion_esperada - fecha_actual).days
        prestamo.dias_restantes = dias_restantes
        prestamo.esta_vencido = dias_restantes < 0
        prestamo.dias_restantes_abs = abs(dias_restantes)
    
    # Historial de préstamos (últimos 5 devueltos)
    historial = Prestamo.objects.filter(
        usuario=request.user,
        fecha_devolucion_real__isnull=False
    ).select_related('libro').order_by('-fecha_devolucion_real')[:5]
    
    context = {
        'perfil': perfil,
        'mis_prestamos': mis_prestamos,
        'historial': historial,
        'total_prestamos_activos': mis_prestamos.count(),
    }
    return render(request, 'panel_usuario.html', context)



@login_exigido
def panel_admin(request):
    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "administrador":
        messages.error(request, "No tienes permisos para acceder a este panel.")
        return redirect("dashboard")

    total_libros = Libro.objects.count()
    total_usuarios = User.objects.count()
    prestamos_activos = Prestamo.objects.filter(fecha_devolucion_real__isnull=True).count()
    multas_totales = Prestamo.objects.filter(multa__gt=0)

    total_multas = sum(p.multa for p in multas_totales)

    context = {
        "total_libros": total_libros,
        "total_usuarios": total_usuarios,
        "prestamos_activos": prestamos_activos,
        "total_multas": total_multas,
    }
    return render(request, "dashboard_admin.html", context)
