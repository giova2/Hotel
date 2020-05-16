from django.db import models

# Create your models here.


class Contenido(models.Model):
    seccion = models.CharField(max_length=40)
    titulo = models.CharField(max_length=40)
    texto = models.CharField(max_length=500)
    def __str__(self):
        return self.seccion

class ImagenesContenido(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='contenido/img')
    def __str__(self):
        return str(self.contenido)
