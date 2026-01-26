from django.db import models

# Create your models here.
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True) # Este será el nombre en la URL (ej: growart)
    color_principal = models.CharField(max_length=7, default="#22c55e") # Código Hexadecimal
    tipografia = models.CharField(max_length=100, default="'Montserrat', sans-serif")
    imagen_fondo = models.ImageField(upload_to='fondos/', null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    # --- REGLAS DE NEGOCIO
    duracion_sesion_base = models.PositiveIntegerField(
        default=8, 
        choices=[(3, '3 Horas'), (5, '5 Horas'), (8, '8 Horas')],
        verbose_name="Duración de Sesión de Estrategia"
    )
    
    permitir_dividir_sesion = models.BooleanField(
        default=True, 
        verbose_name="¿Permitir dividir sesión? (4h + 4h)"
    )
    
    ofrece_drone = models.BooleanField(
        default=False, 
        verbose_name="¿Ofrece servicio de Drone?"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Cliente / Empresa"
        verbose_name_plural = "Clientes / Empresas"