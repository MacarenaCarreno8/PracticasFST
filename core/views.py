from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .models import Postulacion, OfertaLaboral, Perfil, Notificacion, Comentario
from .forms import OfertaLaboralForm, PerfilFormPersonales, PerfilFormAcademicos, PerfilFormAdicionales, PerfilFormHabilidades



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Buscar usuario por email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Correo no encontrado.')
            return redirect('login')

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')

            # Redirige al next si viene desde una página protegida
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('index')
        else:
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('login')
    
    return render(request, 'login.html')

def cargar_notificaciones(request):
    notificaciones = []
    notificaciones_sin_leer = []

    if request.user.is_authenticated and not request.user.is_staff:
        # Simulación de notificaciones
        notificaciones = [
            "Tu postulación a 'Desarrollador Backend' fue aceptada.",
            "Tu postulación a 'QA Tester' fue rechazada."
        ]
        notificaciones_sin_leer = notificaciones  # Simulando no leídas

    return {
        'notificaciones': notificaciones,
        'notificaciones_sin_leer': notificaciones_sin_leer,
    }

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

    ya_postulado = False
    if request.user.is_authenticated and not request.user.is_staff:
        ya_postulado = Postulacion.objects.filter(estudiante=request.user, oferta=oferta).exists()

    return render(request, 'detalle_oferta.html', {
        'oferta': oferta,
        'ya_postulado': ya_postulado
    })

@staff_member_required
def ver_postulantes_oferta(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, pk=oferta_id)
    postulaciones = Postulacion.objects.filter(oferta=oferta).select_related('estudiante')

    return render(request, 'admin_ofertas/postulantes.html', {
        'oferta': oferta,
        'postulaciones': postulaciones
    })

@staff_member_required
def perfil_usuario_admin(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    return render(request, 'admin_ofertas/perfil_usuario.html', {'usuario': usuario})


@login_required
def perfil_usuario(request):
    perfil, creado = Perfil.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form_personales = PerfilFormPersonales(request.POST, request.FILES, instance=perfil)
        form_academicos = PerfilFormAcademicos(request.POST, instance=perfil)
        form_adicionales = PerfilFormAdicionales(request.POST, instance=perfil)
        form_habilidades = PerfilFormHabilidades(request.POST, instance=perfil)

        if 'guardar_personales' in request.POST:
            if form_personales.is_valid():
                form_personales.save()
                messages.success(request, 'Datos personales actualizados correctamente.')
                return redirect('perfil_usuario')

        elif 'guardar_academicos' in request.POST:
            if form_academicos.is_valid():
                form_academicos.save()
                messages.success(request, 'Datos académicos actualizados correctamente.')
                return redirect('perfil_usuario')
            else:
                print(form_academicos.errors)  # Para depurar errores de validación

        elif 'guardar_adicionales' in request.POST:
            if form_adicionales.is_valid():
                form_adicionales.save()
                messages.success(request, 'Datos adicionales actualizados correctamente.')
                return redirect('perfil_usuario')

        elif 'guardar_habilidades' in request.POST:
            if form_habilidades.is_valid():
                form_habilidades.save()
                messages.success(request, 'Datos de habilidades actualizados correctamente.')
                return redirect('perfil_usuario')


    else:
        form_personales = PerfilFormPersonales(instance=perfil)
        form_academicos = PerfilFormAcademicos(instance=perfil)
        form_adicionales = PerfilFormAdicionales(instance=perfil)
        form_habilidades = PerfilFormHabilidades(instance=perfil)


    context = {
        'perfil': perfil,
        'form_personales': form_personales,
        'form_academicos': form_academicos,
        'form_adicionales': form_adicionales,
        'form_habilidades': form_habilidades,
    }

    return render(request, 'perfil.html', context)



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
@require_POST
def postular_oferta(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)
    usuario = request.user

    ya_postulado = Postulacion.objects.filter(estudiante=usuario, oferta=oferta).exists()

    if ya_postulado:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'exito': False, 'mensaje': 'Ya has postulado a esta oferta.'})
        messages.warning(request, 'Ya has postulado a esta oferta.')
        return redirect('detalle_oferta', pk=oferta_id)

    Postulacion.objects.create(estudiante=usuario, oferta=oferta)

    administradores = User.objects.filter(is_staff=True)
    for admin in administradores:
        Notificacion.objects.create(
            usuario=admin,
            mensaje=f"{usuario.username} ha postulado a la oferta '{oferta.titulo}'."
        )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'exito': True, 'mensaje': 'Has postulado exitosamente.'})

    messages.success(request, 'Has postulado exitosamente.')
    return redirect('detalle_oferta', pk=oferta_id)
    
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

@login_required
def mis_postulaciones(request):
    usuario = request.user
    search = request.GET.get('search', '')

    postulaciones = Postulacion.objects.filter(estudiante=usuario).select_related('oferta')

    if search:
        postulaciones = postulaciones.filter(oferta__titulo__icontains=search)

    return render(request, 'mis_postulaciones.html', {
        'postulaciones': postulaciones,
        'search': search,
    })

@login_required
def eliminar_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id, estudiante=request.user)

    if postulacion.estado != 'en_revision':
        messages.error(request, "No puedes eliminar esta postulación porque ya fue procesada.")
        return redirect('mis_postulaciones')

    postulacion.delete()
    messages.success(request, "Postulación eliminada correctamente.")
    return redirect('mis_postulaciones')

def es_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_postulaciones(request):
    ofertas = OfertaLaboral.objects.filter(publicada_por=request.user)
    return render(request, 'admin_postulaciones.html', {'ofertas': ofertas})

@user_passes_test(es_admin)
def ver_postulantes(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id, publicada_por=request.user)
    postulaciones = Postulacion.objects.filter(oferta=oferta)

    return render(request, 'ver_postulantes.html', {
        'oferta': oferta,
        'postulaciones': postulaciones,
    })

@require_POST
@user_passes_test(es_admin)
def cambiar_estado_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    accion = request.POST.get('accion')

    if accion == 'rechazar':
        postulacion.estado = 'rechazado'
        postulacion.save()

        # 🔔 Crear notificación para el estudiante
        Notificacion.objects.create(
            usuario=postulacion.estudiante,
            mensaje=f"Tu postulación a la oferta '{postulacion.oferta.titulo}' fue rechazada."
        )

        return JsonResponse({'success': True})

    elif accion == 'aceptar':
        postulacion.estado = 'aceptado'
        postulacion.save()

        # 🔔 Crear notificación para el estudiante
        Notificacion.objects.create(
            usuario=postulacion.estudiante,
            mensaje=f"¡Felicidades! Tu postulación a la oferta '{postulacion.oferta.titulo}' fue aceptada."
        )

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Acción inválida'}, status=400)


@login_required
@user_passes_test(lambda u: u.is_staff)
def detalle_oferta_popup(request, oferta_id):
    try:
        oferta = OfertaLaboral.objects.get(pk=oferta_id)
    except OfertaLaboral.DoesNotExist:
        oferta = None
    return render(request, 'partials/detalle_oferta_popup.html', {'oferta': oferta})

@login_required
@user_passes_test(lambda u: u.is_staff)
def postulantes_popup(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, pk=oferta_id, publicada_por=request.user)
    postulantes = oferta.postulacion_set.all().select_related('estudiante')
    return render(request, 'partials/postulantes_popup.html', {'oferta': oferta, 'postulantes': postulantes})

@login_required
def eliminar_notificacion(request, noti_id):
    notificacion = get_object_or_404(Notificacion, id=noti_id, usuario=request.user)
    if request.method == "POST":
        notificacion.delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def eliminar_todas_notificaciones(request):
    if request.method == "POST":
        Notificacion.objects.filter(usuario=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@user_passes_test(es_admin)
def resumen_perfil_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    perfil = get_object_or_404(Perfil, user=user)
    html = render_to_string('partials/resumen_perfil_usuario.html', {
        'usuario': user,
        'perfil': perfil
    }, request=request)
    return HttpResponse(html)

def index(request):
    comentarios = Comentario.objects.all().order_by('-fecha')
    
    if request.method == 'POST' and request.user.is_authenticated:
        estrellas = int(request.POST.get('estrellas'))
        texto = request.POST.get('texto')
        Comentario.objects.create(usuario=request.user, estrellas=estrellas, texto=texto)
        return redirect('index')  # o donde tengas tu home
    
    return render(request, 'index.html', {'comentarios': comentarios})