from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading # esto lo usamos para enviar el e-mail de forma asíncrona
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from .models import Reservas, Habitacion, ImagenesHabitacion, EstadosReserva, Contacto
from .forms import ReservasForm, ContactoForm
from contenido.models import Contenido, ImagenesContenido

# Create your views here.


def index(request):
    contenidos = Contenido.objects.filter(seccion__startswith='inicio')
    imagenes_contenido = {}
    for cont in contenidos:
        imagenes_contenido[cont.seccion] = ImagenesContenido.objects.filter(contenido_id= cont.id).first()
    model_habitaciones = Habitacion.objects.all()
    habitaciones = []
    for hab in model_habitaciones:
        habitaciones.append({ 'habitacion': hab, 'imagenes': ImagenesHabitacion.objects.filter(habitacion_id=hab.id) })
    return render(request, 'base_page.html', { 'inicio_header': { 'contenido': contenidos[0] }, 
    'inicio_secundario': { 'contenido': contenidos[1], 'imagen': imagenes_contenido['inicio_secundario'] }, 
    'habitaciones': habitaciones })

def habitacion(request):
    switcher = {
        'GET': habitacionRender
    }
    redirect = switcher.get(request.method, 'No existe tal ruta')
    redirect(request)

# @ensure_csrf_cookie
def habitacionRender(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitacion/habitacion.html', {'habitaciones': habitaciones})

def habitacionList(request):
    habitaciones = Habitacion.objects.all()
    return habitaciones

def reservasRender(request):
    #si se hizo una llamada normal por navegador
    habitaciones = Habitacion.objects.all()
    return render(request, 'reservas/reservas.html', {'habitaciones': habitaciones})

def reservas(request):
    switcher = {
        'GET': reservasList,
        'POST': reservaNew
    }
    redirect = switcher.get(request.method, 'No existe tal ruta')
    return redirect(request)

def reservasList(request):
    # verificamos que haya llegado un id o un status
    idHabitacion = request.GET.get('idHabitacion', default=False)
    estado = request.GET.get('estado', default=False)
    checkin = request.GET.get('checkin', default=False)
    response = Reservas.objects.all()
    if idHabitacion:
        response = response.filter(habitacion_id=idHabitacion)
    if estado:
        response = response.filter(estado=estado)
    if checkin:
        response = response.filter(checkin__gte=checkin) # buscará el checkin que tenga fecha mayor o igual a hoy
    data = list(response.values())
    return JsonResponse(data, safe=False)

def reservaNew(request):
    datos = request.POST.copy()
    # datos['habitacion'] = Habitacion.objects.get(pk=datos['habitacion'])
    tmp_reserva = ReservasForm(datos)
    if tmp_reserva.is_valid():
        # Temporarily make an object to be add some 
        # logic into the data if there is such a need 
        # before writing to the database    
        reserva = tmp_reserva.save(commit = False)
        reserva.estado = EstadosReserva.PENDIENTE.value
        reserva.save()

        send_reserva_mail(reserva)
        # thread = threading.Thread(target=send_reserva_mail, args=(reserva, ))
        # thread.start()

        return JsonResponse({'success': 'Reserva agendada', 'msg': 'hemos tomado su reserva, nos comunicaremos con usted vía e-mail para confirmarla'})
    return JsonResponse({ 'error':tmp_reserva.errors })

def contacto(request):
    switcher = {
        'GET': contactoShow,
        'POST': contactoSend
    }
    redirect = switcher.get(request.method, 'No existe tal ruta')
    return redirect(request)
    
def contactoShow(request):
    return render(request, 'contacto/contacto.html', {})

def contactoSend(request):
    tmp_contacto = ContactoForm(request.POST)
    if tmp_contacto.is_valid():
        contacto = tmp_contacto.save(commit = False)
        contacto.respondido = False

        send_contacto_mail(contacto)
        # thread = threading.Thread(target=send_reserva_mail, args=(reserva, ))
        # thread.start()

        return JsonResponse({ 'success': 'Mensaje enviado'})
    return JsonResponse({ 'error': tmp_contacto.errors})


def send_reserva_mail(reserva):
    template = get_template('email/reserva.html')

    content = template.render({
        'nombre_reserva': reserva.nombre,
        'email': reserva.email,
        'checkin': reserva.checkin,
        'checkout': reserva.checkout,
        'comentarios': reserva.comentarios
    })
    formato = "%d/%m/%y"
    email_message = EmailMultiAlternatives(
        'Reserva solicitada en Budenje complejo de cabañas Entrada: '+str(reserva.checkin.strftime(formato))+' Salida: '+str(reserva.checkout.strftime(formato)), # subject
        '"',
        settings.EMAIL_HOST_USER, #from_email
        [settings.EMAIL_HOST_USER, reserva.email], #to
    )
    email_message.attach_alternative(content, 'text/html')
    email_message.send()

def send_contacto_mail(contacto):
    template = get_template('email/contacto.html')

    content = template.render({
        'asunto': contacto.asunto,
        'nombre': contacto.nombre,
        'email': contacto.email,
        'mensaje': contacto.mensaje
    })  
    email_message = EmailMultiAlternatives(
        'Nuevo mensaje de contacto de '+contacto.nombre, #subject= 
        '"', #body queda vacio
        settings.EMAIL_HOST_USER, # from_email
        [settings.EMAIL_HOST_USER, contacto.email], # to
    )
    email_message.attach_alternative(content, 'text/html')
    email_message.send()