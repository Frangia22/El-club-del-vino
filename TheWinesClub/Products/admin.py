from django.contrib import admin
from Products.models import Categoria, Producto, ComprarProducto, Compra, Pago, Reembolso, DireccionFacturacion

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(ComprarProducto)
admin.site.register(Compra)
admin.site.register(DireccionFacturacion)
admin.site.register(Pago)
admin.site.register(Reembolso)