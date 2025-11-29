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
        # 1. Validación del body
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
        # 2. Registro de usuario
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
        # 3. Inicio de sesión
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
        # 4. Acción no válida
        # ==========================
        return JsonResponse({
            "success": False,
            "error": "Acción no válida"
        }, status=400)
