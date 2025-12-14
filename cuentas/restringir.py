from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps

def role_required(*roles):
    def restringir(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if not hasattr(request.user, "perfil"):
                messages.error(request, "Tu usuario no tiene perfil asociado.")
                return redirect("dashboard")
            if request.user.perfil.rol not in roles:
                messages.error(request, "No tienes permisos para acceder a esta sección.")
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return restringir