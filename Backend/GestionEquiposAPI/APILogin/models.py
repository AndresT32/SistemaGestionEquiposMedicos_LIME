from django.db import models

class Login(models.Model):
    username = models.CharField(primary_key=True, max_length=150, unique=True)
    password = models.CharField(max_length=128)
    rol = models.CharField(max_length=100)

    class Meta:
        db_table = 'login'
