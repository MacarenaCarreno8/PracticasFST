from django.urls import include, path

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

]