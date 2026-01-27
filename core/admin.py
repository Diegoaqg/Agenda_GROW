from django.contrib import admin
from .models import Reserva

# Register your models here.
from django.contrib import admin
from .models import Cliente

admin.site.register(Cliente)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'nombre_contacto', 'fecha_inicio', 'sincronizado_google')
    list_filter = ('sincronizado_google', 'nombre_empresa')