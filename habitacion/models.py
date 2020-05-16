from colorfield.fields import ColorField
from django.db import models
from enum import Enum

SERVICIOS=(
        ('COCINA','Cocina'),
        ('AIRE_CONDICIONADO', 'Aire condicioado'),
        ('DUCHA','Ducha'),
        ('WIFI','Wifi'),
        ('TOALLAS','Toallas'),
    )

class TiposHabitacion(Enum):
    SIMPLE = "Simple"
    DOBLE = "Doble"
    @classmethod
    def all(self):
        return [TiposHabitacion.SIMPLE, TiposHabitacion.DOBLE]


class EstadosReserva(Enum):   # A subclass of Enum
    PENDIENTE = "Pendiente"
    CANCELADA = "Cancelada"
    APROBADA  = "Aprobada"
    @classmethod
    def all(self):
        return [EstadosReserva.PENDIENTE, EstadosReserva.APROBADA, EstadosReserva.CANCELADA]

class EstadosReglas(Enum):   # A subclass of Enum
    ACTIVA   = "Activa"
    INACTIVA = "Inactiva"
    @classmethod
    def all(self):
        return [EstadosReglas.INACTIVA, EstadosReglas.ACTIVA]
# Create your models here.

class Habitacion(models.Model):
    tipo_hab  = models.CharField(
      max_length=10,
      choices=[(tag.value, tag.name) for tag in TiposHabitacion.all()]  # Choices is a list of Tuple
    )
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=500)
    color = ColorField(default="#FF0000")
    class Meta:
        verbose_name_plural = 'Habitaciones'
    def __str__(self):
        return self.nombre

class ImagenesHabitacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.DO_NOTHING)
    imagen = models.ImageField(upload_to='habitacion/img')
    class Meta:
        verbose_name_plural = 'Imagenes Habitaciones'

class ServiciosHabitacion(models.Model):
    habitacion = models.ManyToManyField(Habitacion)
    servicio = models.CharField(max_length=40)
    class Meta:
        verbose_name_plural = 'Servicios Habitaciones'
    def __str__(self):
        return self.servicio

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True)
    telefono = models.CharField(max_length=40)
    email = models.EmailField(max_length=254)
    fecha = models.DateField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.nombre

class Reservas(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True)
    nombre = models.CharField('Nombre de la reserva', max_length=40)
    email = models.EmailField(max_length=254, default="cambiaresteemail@cambio.com")
    checkin = models.DateField('Fecha entrada')
    checkout = models.DateField('Fecha salida')
    estado  = models.CharField('Estado de la reserva',
      max_length=10,
      choices=[(tag.value, tag.name) for tag in EstadosReserva.all()]  # Choices is a list of Tuple
    )
    comentarios = models.CharField(max_length=150, default="Sin comentarios")
    class Meta:
        verbose_name_plural = 'Reservas'
    def __str__(self):
        formato = "%d/%m/%y"
        return self.nombre+' - Entrada: '+str(self.checkin.strftime(formato))+' Salida: '+str(self.checkout.strftime(formato))
    
class Reglas(models.Model):
    nombre         = models.CharField(max_length=50)
    fecha_comienzo = models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin      = models.DateField(auto_now=False, auto_now_add=False)
    estado         = models.CharField(
      max_length=10,
      choices=[(tag.value, tag.name) for tag in EstadosReglas.all()]  # Choices is a list of Tuple
    )
    repetir        = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Reglas'
    def __str__(self):
        return self.nombre

class Contacto(models.Model):
    nombre = models.CharField(max_length=100, default="relleno")
    email = models.EmailField(max_length=254)
    asunto = models.CharField(max_length=100)
    mensaje = models.CharField(max_length=500)
    respondido = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre+' ->respondido: '+self.respondido