from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

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
        

class Reserva(models.Model):
    # --- Datos del Cliente/Empresa ---
    nombre_empresa = models.CharField(max_length=100, verbose_name="Nombre de la Empresa")
    nombre_contacto = models.CharField(max_length=100, verbose_name="Persona de Contacto")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    
    # --- Datos de la Sesión ---
    fecha_inicio = models.DateTimeField(verbose_name="Fecha y Hora de Inicio")
    # Calcularemos el fin automáticamente en la lógica, pero lo guardamos por seguridad
    fecha_fin = models.DateTimeField(verbose_name="Fecha y Hora de Fin")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas adicionales")

    # --- Campos de Control de Google Calendar (El "Blindaje") ---
    # Guardamos el ID que nos da Google para poder editar o borrar la cita después
    google_event_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # Para saber de un vistazo si la sincronización funcionó
    sincronizado_google = models.BooleanField(default=False)
    
    # --- Metadatos ---
    creado_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre_empresa} - {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')}"