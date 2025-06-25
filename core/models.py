from django.db import models
from django.contrib.auth.models import User

class OfertaLaboral(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    modalidad = models.CharField(max_length=50, choices=[
        ('Presencial', 'Presencial'),
        ('Remoto', 'Remoto'),
        ('Híbrido', 'Híbrido'),
        ('Internacional', 'Internacional'),
    ])
    fecha_publicacion = models.DateField(auto_now_add=True)
    publicada_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Postulacion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante.username} - {self.oferta.titulo}"

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, blank=True)
    carrera = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    cv_pdf = models.FileField(upload_to='cvs/', blank=True, null=True)  # Subida de PDF

    def __str__(self):
        return self.usuario.username