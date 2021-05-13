from django.contrib import admin
from .models import Vino, Bodega, Maridaje, Pais

# Register your models here.

admin.site.register(Vino)
admin.site.register(Bodega)
admin.site.register(Pais)
admin.site.register(Maridaje)
