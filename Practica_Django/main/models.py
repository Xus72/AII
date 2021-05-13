from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Bodega(models.Model):

    idBodega = models.TextField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )

class Pais(models.Model):

    idPais = models.TextField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )

class Maridaje(models.Model):

    idMaridaje = models.TextField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('-idMaridaje', )

class Vino(models.Model):

    idVino = models.TextField(primary_key=True)
    nombre = models.CharField(max_length=20)
    anyo = models.IntegerField(verbose_name='Año'
                    , help_text='Debe introducir un año'
                    , validators=[MinValueValidator(1900), MaxValueValidator(2050)]
                    )
    pais = models.ForeignKey(Pais,on_delete=models.SET_NULL, null =True)
    bodega = models.ForeignKey(Bodega,on_delete=models.SET_NULL, null =True)
    maridaje = models.ManyToManyField(Maridaje)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )