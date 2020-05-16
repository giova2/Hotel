from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('habitacion', views.habitacion, name="habitacion"),
    path('contacto', views.contacto, name="contacto"),
    path('reservas', views.reservasRender, name="reservas"),
    path('apireservas', views.reservas),
]
