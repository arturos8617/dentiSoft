import uuid

from django.conf import settings
from django.db import models


# 1. Rol
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

# 2. Clínica
class Clinica(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre


# 3. Paciente
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    es_provisional = models.BooleanField(default=True)
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"

# 4. EstadoCita
class EstadoCita(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=7)  # Ej. "#FF0000"

    def __str__(self):
        return self.nombre

# 5. Cita
class Cita(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.ForeignKey(EstadoCita, on_delete=models.PROTECT)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    dentista = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="citas_dentista",
    )
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cita {self.paciente} con {self.dentista} el {self.fecha} {self.hora}"

# 6. Historial Clínico
class HistorialClinico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    alergias = models.TextField(blank=True)
    condiciones = models.TextField(blank=True)
    medicacion = models.TextField(blank=True)
    notas = models.TextField(blank=True)
    odontograma = models.JSONField(blank=True, null=True)       # placeholder JSON
    periodontograma = models.JSONField(blank=True, null=True)    # placeholder JSON

    def __str__(self):
        return f"Historial de {self.paciente}"

# 7. EstadoTratamiento
class EstadoTratamiento(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.nombre

# 8. Tratamiento
class Tratamiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.ForeignKey(EstadoTratamiento, on_delete=models.PROTECT)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.descripcion[:20]}... ({self.paciente})"

# 9. Pago
class Pago(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    comprobante_adjuntado = models.FileField(upload_to="comprobantes/", blank=True)

    def __str__(self):
        return f"Pago de ${self.monto} - Cita {self.cita.id}"

# 10. InvitacionUsuario
class InvitacionUsuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    token = models.CharField(max_length=255, unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE)
    invitado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="invitaciones_creadas",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("usada", "Usada"),
        ("expirada", "Expirada"),
        ("revocada", "Revocada"),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default="pendiente")

    def __str__(self):
        return f"Invitación {self.email} ({self.estado})"
