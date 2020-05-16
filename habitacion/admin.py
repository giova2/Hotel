from django.contrib import admin
from .models import Habitacion, ImagenesHabitacion, ServiciosHabitacion, Reglas, Reservas, Contacto, Cliente, EstadosReserva
from django.urls import path
from django.core.mail import EmailMessage
from django.http import JsonResponse

admin.site.site_header = "Budenje administración"
# admin.site.site_title  = "Bud-admin"
admin.site.index_title = "Bud-admin: Administre sus reservas y contenido del sitio"

class ImagenesHabitacionInline(admin.StackedInline):
    model = ImagenesHabitacion

class ServiciosHabitacionInline(admin.TabularInline):
    model = ServiciosHabitacion.habitacion.through #usamos esto debido a que es una relacion muchos a muchos

class HabitacionAdmin(admin.ModelAdmin):
    inlines = [ImagenesHabitacionInline, ServiciosHabitacionInline,]
    exclude = ('habitacion',)

# personalizar admin
class ReservasAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'checkin', 'checkout', 'estado',)
    list_filter = ('checkin','checkout','estado',)
    class Media:
        js = ("habitacion/js/admin/reservas.js",)
    
    def save_model(self, request, obj, form, change):
        estado = form.cleaned_data.get('estado')
        print(estado)
        if 'estado' in form.changed_data and estado != EstadosReserva.PENDIENTE.value:
            print('enviar e-mail')
            switch_body = {
                EstadosReserva.APROBADA.value : "<h3>Reserva Aprobada</h3> <br><p>Su Reserva fue aprobada. Lo esperamos a partir de las 10 AM para realizar el checkin</p>",
                EstadosReserva.CANCELADA.value: "<p>Lamentamos informarle que su reserva fue <strong>cancelada</strong> por los siguientes motivos "+form.cleaned_data.get('comentarios')+" disculpe las molestias ocasionadas.</p>"
            }
            body = switch_body[estado]
            body = body + "<p>Saludos, Equipo de Budenje.</p>"
            formato = "%d/%m/%y"
            email_message = EmailMessage(
                subject='ESTADO DE RESERVA:'+ form.cleaned_data.get('estado') +'Reserva solicitada en Budenje complejo de cabañas Entrada: '+str(form.cleaned_data.get('checkin').strftime(formato))+' Salida: '+str(form.cleaned_data.get('checkout').strftime(formato)),
                body= body,
                from_email='mydefaultemail@default.com',
                to=['mydefaultemail@default.com', form.cleaned_data.get('email')],
            )
            email_message.content_subtype = 'html'
            email_message.send()
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Habitacion, HabitacionAdmin)
admin.site.register(ServiciosHabitacion)
admin.site.register(Reglas)
admin.site.register(Reservas, ReservasAdmin)
admin.site.register(Contacto)
admin.site.register(Cliente)
