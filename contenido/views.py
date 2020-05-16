from django.shortcuts import render
from .models import Contenido, ImagenesContenido
# Create your views here.
def nosotros(request):
    contenidos = Contenido.objects.filter(seccion='nosotros')
    nosotros = []
    for cont in contenidos:
        nosotros.append({ 'item': cont, 'imagen': ImagenesContenido.objects.filter(contenido_id= cont.id).first() })
    return render(request, 'nosotros/nosotros.html', { 'contenidos' : nosotros })