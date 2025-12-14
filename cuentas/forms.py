from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario

class CrearBibliotecarioForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    rut = forms.CharField(max_length=12, required=False)
    direccion = forms.CharField(required=False)
    telefono = forms.CharField(required=False)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Las contraseñas no coinciden.")
        if User.objects.filter(username=cleaned.get("username")).exists():
            raise forms.ValidationError("Ese username ya existe.")
        return cleaned

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data["username"],
            email=data.get("email", ""),
            password=data["password1"],
        )
        PerfilUsuario.objects.create(
            user=user,
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
