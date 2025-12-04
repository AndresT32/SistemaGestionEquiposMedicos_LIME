from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from .models import Login

@receiver(post_migrate)
def crear_admin_automatico(sender, **kwargs):
    # Evita que corra en apps diferentes
    if sender.name != "APILogin":
        return

    # Crear superusuario para login normal
    if not Login.objects.filter(username="ADMINISTRADOR").exists():
        Login.objects.create(
            username="ADMINISTRADOR",
            password=make_password("admin123"),  # Contraseña por defecto
            rol="admin",
        )
        print("⚡ Usuario ADMINISTRADOR creado automáticamente.")