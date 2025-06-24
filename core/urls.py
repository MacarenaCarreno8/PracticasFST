from django.urls import include, path

from . import views

urlpatterns= [
    path('', views.index, name="index"),
    path('registrarse/', views.registrarse, name="registrarse"),
    path ('login/', views.login, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

]