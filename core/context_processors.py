from .models import Notificacion

def notificaciones_context(request):
    if request.user.is_authenticated:
        # Mostrar notificaciones para cualquier usuario autenticado
        notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-id')
        notificaciones_sin_leer = notificaciones.filter(leida=False)
    else:
        notificaciones = []
        notificaciones_sin_leer = []

    return {
        'notificaciones': notificaciones,
        'notificaciones_sin_leer': notificaciones_sin_leer
    }
