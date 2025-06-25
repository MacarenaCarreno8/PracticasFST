from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Postulacion, OfertaLaboral
from .forms import OfertaLaboralForm


def index (request):
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Buscar al usuario por email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Correo no encontrado.')
            return redirect('login')

        # Autenticar
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('index')  # O a donde desees redirigir
        else:
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('login')
    
    return render(request, 'login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

def oportunidades(request):
    ofertas = OfertaLaboral.objects.all()

    # Obtener filtros desde GET
    cargo = request.GET.get('cargo')
    modalidad = request.GET.get('modalidad')

    if cargo:
        # Filtrar por título (nombre del cargo)
        ofertas = ofertas.filter(titulo__icontains=cargo)

    if modalidad:
        ofertas = ofertas.filter(modalidad=modalidad)

    context = {
        'ofertas': ofertas,
        'modalidades': ['Presencial', 'Remoto', 'Híbrido', 'Internacional'],
        'filtro_cargo': cargo or '',
        'filtro_modalidad': modalidad or '',
    }
    return render(request, 'oportunidades.html', context)

def detalle_oferta(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk)
    return render(request, 'detalle_oferta.html', {'oferta': oferta})

@login_required
def perfil_usuario(request):
    return render(request, 'perfil.html')

@staff_member_required
def publicaciones_admin(request):
    return render(request, 'admin_publicaciones.html')

@login_required
def mi_curriculum(request):
    return render(request, 'mi_curriculum.html')

def registrarse (request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validar que las contraseñas coincidan
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registrarse')

        # Validar que el nombre de usuario no exista
        if User.objects.filter(username=nombre).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
            return redirect('registrarse')

        # Validar que el correo no exista
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ese correo electrónico ya está registrado.')
            return redirect('registrarse')

        # Crear el usuario
        user = User.objects.create_user(username=nombre, email=email, password=password1)
        user.save()
        messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request,'registrarse.html')

@login_required
def lista_ofertas(request):
    ofertas = OfertaLaboral.objects.all()
    return render(request, 'ofertas.html', {'ofertas': ofertas})

@login_required
def mis_postulaciones(request):
    usuario = request.user  # usuario autenticado
    postulaciones = Postulacion.objects.filter(estudiante=usuario).select_related('oferta')
    
    return render(request, 'mis_postulaciones.html', {
        'postulaciones': postulaciones
    })

@login_required
def postular_oferta(request, oferta_id):
    oferta = OfertaLaboral.objects.get(id=oferta_id)
    usuario = request.user

    # Verificamos si ya está postulando
    ya_postulado = Postulacion.objects.filter(estudiante=usuario, oferta=oferta).exists()
    if ya_postulado:
        messages.warning(request, 'Ya has postulado a esta oferta.')
    else:
        Postulacion.objects.create(estudiante=usuario, oferta=oferta)
        messages.success(request, 'Has postulado exitosamente.')

    return redirect('ofertas')

    
    #CRUD ADMINISTRADOR

def es_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(es_admin)
def lista_ofertas(request):
    ofertas = OfertaLaboral.objects.all().order_by('-fecha_publicacion')
    return render(request, 'admin_ofertas/lista.html', {'ofertas': ofertas})

@login_required
@user_passes_test(es_admin)
def crear_oferta(request):
    if request.method == 'POST':
        form = OfertaLaboralForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.publicada_por = request.user
            oferta.save()
            return redirect('lista_ofertas')
    else:
        form = OfertaLaboralForm()
    return render(request, 'admin_ofertas/formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_admin)
def editar_oferta(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk)
    form = OfertaLaboralForm(request.POST or None, instance=oferta)
    if form.is_valid():
        form.save()
        return redirect('lista_ofertas')
    return render(request, 'admin_ofertas/formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_admin)
def eliminar_oferta(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk)
    if request.method == 'POST':
        oferta.delete()
        return redirect('lista_ofertas')
    return render(request, 'admin_ofertas/confirmar_eliminar.html', {'oferta': oferta})