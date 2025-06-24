from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def index (request):
    return render(request,'index.html')

def login (request):
    return render(request,'login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

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

