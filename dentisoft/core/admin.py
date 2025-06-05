from django.contrib import admin
from .models import (
    Rol, Clinica, Paciente, EstadoCita, Cita,
    HistorialClinico, EstadoTratamiento, Tratamiento,
    Pago, InvitacionUsuario
)

admin.site.register(Rol)
admin.site.register(Clinica)
admin.site.register(Paciente)
admin.site.register(EstadoCita)
admin.site.register(Cita)
admin.site.register(HistorialClinico)
admin.site.register(EstadoTratamiento)
admin.site.register(Tratamiento)
admin.site.register(Pago)
admin.site.register(InvitacionUsuario)
