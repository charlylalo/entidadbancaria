from django.contrib import admin

from .models import Asesor, Cliente, Cuenta, Transacciones, Financiamiento

# Register your models here.

admin.site.register(Asesor)
admin.site.register(Cliente)
admin.site.register(Cuenta)
admin.site.register(Transacciones)
admin.site.register(Financiamiento)