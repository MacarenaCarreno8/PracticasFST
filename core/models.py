from django.db import models
from django.contrib.auth.models import User

class AreaInteres(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

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
    
    # Nuevos campos para ubicación
    ciudad = models.CharField(max_length=100, default='Santiago')  # puedes dejar fija Santiago o cambiar
    comuna = models.CharField(max_length=100, choices=[
        ('Santiago', 'Santiago'),
        ('Las Condes', 'Las Condes'),
        ('Providencia', 'Providencia'),
        ('Maipú', 'Maipú'),
        ('La Florida', 'La Florida'),
        ('Puente Alto', 'Puente Alto'),
        ('Ñuñoa', 'Ñuñoa'),
        ('Recoleta', 'Recoleta'),
        ('La Reina', 'La Reina'),
        # Agrega las comunas que quieras de RM
    ], default='Santiago')

    def __str__(self):
        return self.titulo

class Postulacion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    
    ESTADOS = [
        ('en_revision', 'En revisión'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_revision')

    def __str__(self):
        return f"{self.estudiante.username} - {self.oferta.titulo}"


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100, blank=True)
    pais_residencia = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    TIPO_DOCUMENTO = [
        ('CI', 'Cédula de Identidad'),
        ('PAS', 'Pasaporte'),
    ]
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO, blank=True)
    numero_documento = models.CharField(max_length=50, blank=True)
    
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True)
    
    telefono = models.CharField(max_length=20, blank=True)
    carrera = models.CharField(max_length=150, blank=True)
    curriculum_pdf = models.FileField(upload_to='cv/', null=True, blank=True)

    # Campos académicos que faltan:
    pais_institucion = models.CharField(max_length=100, blank=True)
    nivel_academico = models.CharField(max_length=50, blank=True)
    area_estudio = models.CharField(max_length=100, blank=True)
    carrera_pregrado = models.CharField(max_length=150, blank=True)
    SITUACION_ACADEMICA_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('titulado', 'Titulado'),
    ]
    situacion_academica = models.CharField(max_length=20, choices=SITUACION_ACADEMICA_CHOICES, blank=True)
    ANIO_ESTUDIO_CHOICES = [
        ('1', 'Primer año'),
        ('2', 'Segundo año'),
        ('3', 'Tercer año'),
        ('4', 'Cuarto año'),
        ('5', 'Quinto año'),
    ]
    anio_estudio = models.CharField(max_length=2, choices=ANIO_ESTUDIO_CHOICES, blank=True)

    ESTOY_BUSCANDO_CHOICES = [
        ('practica', 'Práctica y/o pasantía'),
        ('trabajo', 'Trabajo'),
    ]
    estoy_buscando = models.CharField(max_length=20, choices=ESTOY_BUSCANDO_CHOICES, blank=True)

    EXPERIENCIA_CHOICES = [
        ('sin_exp', 'Sin experiencia'),
        ('1_ano', '1 año'),
        ('2_anos', '2 años'),
    ]
    experiencia_laboral = models.CharField(max_length=20, choices=EXPERIENCIA_CHOICES, blank=True)

    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('medio', 'Medio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]

    NIVEL_INGLES_CHOICES = [
        ('basico', 'Básico'),
        ('medio', 'Medio'),
        ('avanzado', 'Avanzado'),
        ('nativo', 'Nativo'),
    ]

    nivel_excel = models.CharField(max_length=10, choices=NIVEL_CHOICES, blank=True)
    nivel_ingles = models.CharField(max_length=10, choices=NIVEL_INGLES_CHOICES, blank=True)

    # Aquí agregamos el ManyToManyField para múltiples áreas de interés
    areas_interes = models.ManyToManyField(AreaInteres, blank=True)

class Postulacion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
