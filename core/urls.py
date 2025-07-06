from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns= [
    path('', views.index, name="index"),
    path('registrarse/', views.registrarse, name="registrarse"),
    path ('login/', views.login, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('ofertas/', views.lista_ofertas, name='ofertas'),
    path('postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('postular/<int:oferta_id>/', views.postular_oferta, name='postular_oferta'),
    path('panel/publicaciones/', views.publicaciones_admin, name='publicaciones_admin'),
    path('curriculum/', views.mi_curriculum, name='mi_curriculum'),
    path('publicaciones/', views.lista_ofertas, name='lista_ofertas'),
    path('publicaciones/crear/', views.crear_oferta, name='crear_oferta'),
    path('publicaciones/editar/<int:pk>/', views.editar_oferta, name='editar_oferta'),
    path('publicaciones/eliminar/<int:pk>/', views.eliminar_oferta, name='eliminar_oferta'),
    path('oportunidades/', views.oportunidades, name='oportunidades'),
    path('oportunidades/<int:pk>/', views.detalle_oferta, name='detalle_oferta'),
    path('admin/oferta/<int:oferta_id>/postulantes/', views.ver_postulantes_oferta, name='ver_postulantes_oferta'),
    path('admin/usuario/<int:user_id>/', views.perfil_usuario_admin, name='perfil_usuario_admin'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('mis-postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),
    path('eliminar-postulacion/<int:postulacion_id>/', views.eliminar_postulacion, name='eliminar_postulacion'),
    path('postulaciones/eliminar/<int:postulacion_id>/', views.eliminar_postulacion, name='eliminar_postulacion'),
    path('panel/postulaciones/', views.admin_postulaciones, name='admin_postulaciones'),
    path('panel/oferta/<int:oferta_id>/postulantes/', views.ver_postulantes, name='ver_postulantes'),
    path('panel/postulacion/<int:postulacion_id>/estado/', views.cambiar_estado_postulacion, name='cambiar_estado_postulacion'),
    path('panel/oferta/<int:oferta_id>/detalle-popup/', views.detalle_oferta_popup, name='detalle_oferta_popup'),
    path('panel/oferta/<int:oferta_id>/postulantes-popup/', views.postulantes_popup, name='postulantes_popup'),
    path('notificaciones/eliminar/<int:noti_id>/', views.eliminar_notificacion, name='eliminar_notificacion'),
    path('notificaciones/eliminar_todas/', views.eliminar_todas_notificaciones, name='eliminar_todas_notificaciones'),
    path('perfil/resumen/<int:user_id>/', views.resumen_perfil_usuario, name='resumen_perfil_usuario'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)