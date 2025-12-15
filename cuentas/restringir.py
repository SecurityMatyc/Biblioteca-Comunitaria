from django.contrib.auth import REDIRECT_FIELD_NAME
def login_exigido(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.core.exceptions import PermissionDenied

def role_required(*roles):
    def restringir(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not hasattr(request.user, "perfil"):
                raise PermissionDenied
            if request.user.perfil.rol not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return restringir