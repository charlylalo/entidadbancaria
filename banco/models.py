from django.db import models
from django.urls import reverse

# Create your models here.

class Cliente(models.Model):
  nombre = models.CharField(max_length=20)
  apellido_paterno = models.CharField(max_length= 20)
  apellido_materno = models.CharField(max_length= 20)
  fecha_registro = models.DateField()
  email = models.CharField(max_length=30)

  def __str__(self):
        return f'{self.nombre} ({self.apellido_paterno})'
  
  def get_absolute_url(self):
        return reverse('detalle-cliente', args=[str(self.pk)])
  
class Asesor(models.Model):  
  nombre = models.CharField(max_length=20)
  apellido_paterno = models.CharField(max_length= 20)
  apellido_materno = models.CharField(max_length= 20)

  def __str__(self):
      return f'{self.nombre} ({self.apellido_paterno})'
  
  def get_absolute_url(self):
        return reverse('detalle-asesor', args=[str(self.pk)])
  
import uuid

class Cuenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    cliente = models.ForeignKey(Cliente , on_delete = models.CASCADE)
    asesor = models.ManyToManyField(Asesor)
    feha_creacion = models.DateField()

    ACCOUNT_STATUS = (
      ('a', 'Activa'),
      ('i', 'Inactiva'),
      ('b', 'Baja'),
      ('c', 'Cerrada'),
    )

    status = models.CharField(
        max_length=1,
        choices=ACCOUNT_STATUS,
        default='a',
    )

    TYPE_ACCOUNT = (
      ('c', 'Corriente'),
      ('n', 'Nómina'),
      ('a', 'Ahorro'),
    )

    tipo_cuenta = models.CharField(
        max_length=1,
        choices=TYPE_ACCOUNT,
        default='c',
    )

    balance = models.DecimalField(decimal_places = 2, max_digits = 10)

    def __str__(self):
      return f'cuenta {self.id}'
  
    def get_absolute_url(self):
        return reverse('detalle-cuenta', args=[str(self.pk)])
        
class Transacciones(models.Model):
    
    cuenta = models.ForeignKey(Cuenta, on_delete = models.RESTRICT)
    fecha = models.DateField()
    cantidad = models.DecimalField(decimal_places = 2, max_digits = 10)

    TYPE = (
        ('n', 'Pago de Nómina'),
        ('p', 'Pago a proveedores'),
        ('r', 'Reembolso de gastos'),
        ('t', 'Traslado de efectivo entre entidades bancarias')
    )

    tipo = models.CharField(
        max_length=1,
        choices=TYPE,
        default='pn'
    )

    cuenta_origen = models.CharField(max_length = 10)

    def __str__(self):
      return f'transacción ${self.pk}'
  
    def get_absolute_url(self):
        return reverse('detalle-transaccion', args=[str(self.pk)])

class Financiamiento(models.Model):
    
    cuenta = models.ManyToManyField(Cuenta)

    FINANCING_TYPES = (
        ('p', 'Préstamo'),
        ('c', 'Crédito'),
    )

    tipo_financiamiento = models.CharField(
        max_length=1,
        choices= FINANCING_TYPES,
        default='c'
    )

    cantidad_prestamo = models.DecimalField(decimal_places = 2, max_digits = 10, null=True, blank=True )
    plazo= models.IntegerField(null=True, blank = True)
    tasa_interes = models.DecimalField(decimal_places = 2, max_digits = 10, null=True, blank = True)

    def __str__(self):
      return f'Financiamiento ${self.cuenta}'
  
    def get_absolute_url(self):
        return reverse('detalle-financiamiento', args=[str(self.pk)])
