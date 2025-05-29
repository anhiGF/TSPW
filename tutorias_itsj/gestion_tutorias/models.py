from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('Estudiante', 'Estudiante'),
        ('Tutor', 'Tutor'),
        ('Administrador', 'Administrador'),
    ]
    
    num_control = models.IntegerField(primary_key=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    semestre = models.SmallIntegerField(blank=True, null=True)
    fecha_nac = models.DateField(blank=True, null=True)
    tipo_usuario = models.CharField(max_length=13, choices=TIPO_USUARIO_CHOICES)
    fecha_registro = models.DateField(auto_now_add=True)
    ultima_sesion = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.num_control})"

class RecuperacionContraseña(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=64)
    expira_en = models.DateTimeField()

class Tutoria(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]
    
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    duracion = models.IntegerField(help_text="Duración en minutos")
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    tutor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tutorias_como_tutor')
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tutorias_como_estudiante')
    promedio_calificacion = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.fecha}"

class HistorialModificaciones(models.Model):
    tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Historial de modificaciones"

class Mensaje(models.Model):
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    
    def __str__(self):
        return f"De {self.remitente} a {self.destinatario} - {self.fecha_envio}"

class Evaluacion(models.Model):
    puntaje = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Evaluación de {self.tutoria} - {self.puntaje} estrellas"

class Recurso(models.Model):
    TIPO_CHOICES = [
        ('Documento', 'Documento'),
        ('Enlace', 'Enlace'),
        ('Video', 'Video'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=255)
    tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='recursos_tutorias/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo} para {self.tutoria}"

class Feedback(models.Model):
    comentario = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tutoria = models.ForeignKey(Tutoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Feedback de {self.usuario} sobre {self.tutoria}"