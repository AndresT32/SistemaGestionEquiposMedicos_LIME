from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import Login
import json

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):

    def get(self, request, id=None):
        if id:
            users = list(Login.objects.filter(id=id).values())
            if users:
                return JsonResponse({"message": "Success", "user": users[0]})
            return JsonResponse({"message": "User not found"}, status=404)

        users = list(Login.objects.values())
        return JsonResponse({"message": "Success", "users": users})

    def post(self, request):

        # -----------------------------
        # 1. Validación del body JSON
        # -----------------------------
        try:
            data = json.loads(request.body.decode('utf-8'))
        except:
            return JsonResponse({
                "success": False,
                "error": "JSON inválido o vacío"
            }, status=400)

        accion = data.get("accion")
        username = data.get("username")
        password = data.get("password")
        rol = data.get("rol")

        # ==========================
        # A. Validar clave registro
        # ==========================
        if accion == "validar_registro":
            clave = data.get("clave")

            admin = Login.objects.filter(rol="admin").first()

            if not admin:
                return JsonResponse({
                    "success": False,
                    "error": "No existe un usuario con rol ADMIN en la base"
                }, status=404)

            if check_password(clave, admin.password):
                return JsonResponse({"success": True})

            return JsonResponse({
                "success": False,
                "error": "Clave de administrador incorrecta"
            })
        # ==========================
        # B. Registrar usuario nuevo
        # ==========================
        if accion == "registro":

            if Login.objects.filter(username=username).exists():
                return JsonResponse({
                    "success": False,
                    "error": "El usuario ya existe"
                }, status=400)

            Login.objects.create(
                username=username,
                password=make_password(password),
                rol=rol
            )

            return JsonResponse({
                "success": True,
                "message": "Usuario registrado correctamente"
            })

        # ==========================
        # C. Login
        # ==========================
        if accion == "login":

            try:
                user = Login.objects.get(username=username)
            except Login.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "error": "Usuario no encontrado"
                }, status=404)

            if check_password(password, user.password):
                return JsonResponse({
                    "success": True,
                    "usuario": username,
                    "rol": user.rol,
                    "mensaje": "Inicio de sesión exitoso"
                })

            return JsonResponse({
                "success": False,
                "error": "Contraseña incorrecta"
            }, status=401)

        # ==========================
        # D. Cambiar contraseña ADMIN
        # ==========================
        if accion == "cambiar_password_admin":

            password_actual = data.get("password_actual")
            password_nueva = data.get("password_nueva")

            if not (password_actual and password_nueva):
                return JsonResponse({
                    "success": False,
                    "error": "Datos incompletos"
                }, status=400)

            admin = Login.objects.filter(rol="admin").first()

            if not admin:
                return JsonResponse({
                    "success": False,
                    "error": "No existe un usuario con rol ADMIN"
                }, status=404)

            if not check_password(password_actual, admin.password):
                return JsonResponse({
                    "success": False,
                    "error": "La contraseña actual es incorrecta"
                }, status=401)

            admin.password = make_password(password_nueva)
            admin.save()

            return JsonResponse({
                "success": True,
                "message": "Contraseña actualizada correctamente"
            })
        # ==========================
        # E. Acción no válida
        # ==========================
        return JsonResponse({
            "success": False,
            "error": "Acción no válida"
        }, status=400)
