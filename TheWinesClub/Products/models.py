from django.conf import settings
from django.db import models
from django.urls import reverse
from datetime import date, time, timedelta, timezone
from Products.listas import tipo_vino, variedad_vino, direccion
from django_countries.fields import CountryField

# Create your models here.
class Categoria(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.titulo

class Producto(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.AutoField(primary_key=True)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    imagen = models.ImageField()
    precio = models.PositiveIntegerField()
    precio_rebajdo = models.PositiveIntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    categorias = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)
    productor = models.CharField(max_length=100)
    tipo = models.CharField(choices=tipo_vino, max_length=1)
    variedad = models.CharField(choices=variedad_vino, max_length=10)
    corte = models.CharField(max_length=50)
    alcohol = models.CharField(max_length=8)

    def __str__(self):
        return self.titulo
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})

class ComprarProducto(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comprar = models.BooleanField(default=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        # pylint: disable=E1101
        return f"{self.cantidad} of {self.producto.titulo}"

    def get_total_precio_producto(self):
        # pylint: disable=E1101
        return self.cantidad * self.producto.precio

    def get_guardar_cantidad(self):
        return self.get_total_precio_producto()

    def get_precio_final(self):
        return self.get_total_precio_producto()
class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    productos = models.ManyToManyField(ComprarProducto)
    fecha =models.DateTimeField(auto_now_add=True)
    fecha_compra =models.DateTimeField()
    comprar =models.BooleanField(default=False)
    direccion_envio =models.ForeignKey('DireccionFacturacion', related_name='DireccionEnvio', on_delete=models.SET_NULL, blank=True, null=True)
    direccion_facturacion =models.ForeignKey('DireccionFacturacion', related_name='DireccionFacturacion', on_delete=models.SET_NULL, blank=True, null=True)
    pago =models.ForeignKey('Pago', on_delete=models.SET_NULL, blank=True, null=True)
    pedido_enviado =models.BooleanField(default=False)
    recibido =models.BooleanField(default=False)
    reembolso_solicitado =models.BooleanField(default=False)
    reembolso_aceptado =models.BooleanField(default=False)

class DireccionFacturacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calle = models.CharField(max_length=100)
    numero_calle = models.CharField(max_length=20)
    country = CountryField(multiple= False)
    tipo_direccion = models.CharField(max_length=1, choices=direccion)

    class Meta:
        verbose_name_plural = 'DireccionesFacturacion'

class Pago(models.Model):
    id_carga_banda = models.CharField(max_length=50)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    tiempo = models.DateTimeField(auto_now_add=True)

class Reembolso(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    razon = models.TextField()
    aceptado = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
        
        
        
        
        

    
    
    
