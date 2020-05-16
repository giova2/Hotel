from django.contrib import admin
from .models import Contenido, ImagenesContenido


class ImagenesContenidoInline(admin.StackedInline):
    model = ImagenesContenido

class ContenidoAdmin(admin.ModelAdmin):
    inlines = [ImagenesContenidoInline,]
    list_display  = ('seccion', 'titulo', 'texto',)


# Register your models here.
admin.site.register(Contenido, ContenidoAdmin)
# admin.site.register(ImagenesContenido)