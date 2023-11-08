from django.http import HttpResponse
from django.shortcuts import redirect, render
from orders.forms import PizzaForm
from orders.models import Pizza
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm

def start(request):
    return render(request, 'index.html')

def carrito(request):
    return render(request, 'carrito.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('start')
        else:
            # Muestra un mensaje de error en caso de credenciales incorrectas
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('start')
        else:
            messages.error(request, 'Hubo un error en el registro. Por favor, corrige los errores a continuación.')
            # Devuelve la plantilla 'register.html' junto con el formulario y los mensajes de error
            return render(request, 'register.html', {'form': form})        
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Create your views here.
def home(request):
    return HttpResponse("Bienvenido a Pinocchio's Pizza & Subs")

def index(request):
    if request.method == 'POST':
        # Procesar el formulario si se ha enviado
        form = PizzaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la nueva pizza en la base de datos
            return redirect('menu')  # Redirige a la página del menú después de agregar la pizza
    else:
        # Muestra el formulario vacío si no se ha enviado
        form = PizzaForm()
    # Recupera todas las pizzas desde la base de datos
    pizzas = Pizza.objects.all()

    # Pasa las pizzas y el formulario a la plantilla para su renderización
    return render(request, 'menu.html', {'pizzas': pizzas, 'form': form})