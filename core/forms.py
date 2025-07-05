from django import forms
from .models import OfertaLaboral, Perfil, AreaInteres

class OfertaLaboralForm(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
        fields = ['titulo', 'descripcion', 'modalidad', 'ciudad', 'comuna']  # agregados ciudad y comuna
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            # Puedes personalizar el widget de ciudad o comuna si quieres:
            # 'comuna': forms.Select(attrs={'class': 'form-control'}),
            # 'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'foto', 'nombres', 'apellidos', 'nacionalidad', 'pais_residencia',
            'fecha_nacimiento', 'tipo_documento', 'numero_documento',
            'genero', 'telefono', 'carrera', 'curriculum_pdf'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'pais_residencia': forms.Select(choices=[('', 'Selecciona un país')] + [(p, p) for p in ['Chile', 'Argentina', 'Perú', 'Colombia', 'México']]),
        }

from django import forms
from .models import Perfil

class PerfilFormPersonales(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto', 'nombres', 'apellidos', 'nacionalidad', 'pais_residencia', 'fecha_nacimiento', 'tipo_documento', 'numero_documento', 'genero', 'telefono']

class PerfilFormAcademicos(forms.ModelForm):
    NIVEL_ACADEMICO_CHOICES = [
        ('TSI', 'Técnico superior incompleta'),
        ('TSC', 'Técnico superior completa'),
        ('PI', 'Profesional incompleta'),
        ('PC', 'Profesional completa'),
    ]

    SITUACION_ACADEMICA_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('egresado', 'Egresado'),
        ('titulado', 'Titulado'),
    ]

    ANIO_ESTUDIO_CHOICES = [
        ('1', 'Primer año'),
        ('2', 'Segundo año'),
        ('3', 'Tercer año'),
        ('4', 'Cuarto año'),
        ('5', 'Quinto año'),
    ]

    nivel_academico = forms.ChoiceField(choices=NIVEL_ACADEMICO_CHOICES, required=False)
    situacion_academica = forms.ChoiceField(choices=SITUACION_ACADEMICA_CHOICES, widget=forms.RadioSelect, required=False)
    anio_estudio = forms.ChoiceField(choices=ANIO_ESTUDIO_CHOICES, required=False)

    class Meta:
        model = Perfil
        fields = ['pais_institucion', 'nivel_academico', 'area_estudio', 'carrera_pregrado', 'situacion_academica', 'anio_estudio']
        widgets = {
            'situacion_academica': forms.RadioSelect(),
        }

class PerfilFormAdicionales(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['estoy_buscando', 'experiencia_laboral']
        widgets = {
            'estoy_buscando': forms.Select(attrs={'class': 'form-control'}),
            'experiencia_laboral': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'estoy_buscando': 'Estoy buscando',
            'experiencia_laboral': 'Experiencia laboral',
        }

class PerfilFormHabilidades(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nivel_excel', 'nivel_ingles']
        widgets = {
            'nivel_excel': forms.Select(attrs={'class': 'form-control'}),
            'nivel_ingles': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nivel_excel': 'Nivel de Excel',
            'nivel_ingles': 'Nivel de Inglés',
        }

class PerfilFormAreasInteres(forms.ModelForm):
    areas_interes = forms.ModelMultipleChoiceField(
        queryset=AreaInteres.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Áreas de interés"
    )

    class Meta:
        model = Perfil
        fields = ['areas_interes']