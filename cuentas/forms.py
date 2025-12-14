from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario

class CrearBibliotecarioForm(forms.Form):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    rut = forms.CharField(max_length=15, required=True)
    direccion = forms.CharField(required=False)
    telefono = forms.CharField(required=False)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        rut = cleaned.get("rut")
        # Limpiar puntos del rut para validación y guardado
        if rut:
            rut = rut.replace('.', '').replace(' ', '')
            cleaned["rut"] = rut
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")
        # Validar que el email no esté repetido
        if not email:
            raise forms.ValidationError("El correo es obligatorio.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ese correo ya está registrado.")
        # Validar formato de correo (ya lo hace EmailField, pero por si acaso)
        if "@" not in email or "." not in email:
            raise forms.ValidationError("Ingrese un correo electrónico válido.")
        # Validar que el rut no esté repetido
        if not rut:
            raise forms.ValidationError("El RUT es obligatorio.")
        if PerfilUsuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Ese RUT ya está registrado.")
        # Validar formato de RUT chileno (con o sin puntos, con guion)
        import re
        rut_regex = r"^(\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]|\d{7,8}-[\dkK])$"
        if not re.match(rut_regex, cleaned.get("rut")):
            raise forms.ValidationError("Ingrese un RUT válido (Ej: 12.345.678-9 o 12345678-K)")
        # Validar contraseñas
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        if not password1 or len(password1) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if password1.isdigit() or password1.isalpha():
            raise forms.ValidationError("La contraseña debe contener letras y números.")
        # Puede agregar más validaciones si se requiere
        return cleaned

    def save(self):
        data = self.cleaned_data
        email = data.get("email", "")
        # Generar username automáticamente desde el email
        username = email.split('@')[0].replace('.', '_')
        contador = 1
        username_original = username
        while User.objects.filter(username=username).exists():
            username = f"{username_original}{contador}"
            contador += 1
        user = User.objects.create_user(
            username=username,
            email=email,
            password=data["password1"],
        )
        PerfilUsuario.objects.create(
            usuario=user,
            rol="bibliotecario",
            rut=data.get("rut", ""),
            direccion=data.get("direccion", ""),
            telefono=data.get("telefono", ""),
        )
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
