from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from orders.forms import PizzaForm
from orders.models import Pizza
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm

def start(request):
    return render(request, 'index.html')

def carrito(request):
    return render(request, 'carrito.html')

def add_to_cart(request, pizza_id):
    pizza = get_object_or_404(Pizza, pk=pizza_id)

    # Aquí puedes implementar la lógica para agregar la pizza al carrito
    # Puedes utilizar sesiones o un modelo de carrito de compras para hacer esto

    return redirect('menu') 

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
        form = PizzaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = PizzaForm()

    # Recupera todas las pizzas desde la base de datos
    pizzas = Pizza.objects.all()
    
    # Separa las pizzas por tamaño
    pizzas_familiares = pizzas.filter(size=12)
    pizzas_grandes = pizzas.filter(size=8)
    pizzas_medianas = pizzas.filter(size=6)
    pizzas_slice = pizzas.filter(size=4)

    return render(request, 'menu.html', {
        'pizzas_familiares': pizzas_familiares,
        'pizzas_grandes': pizzas_grandes,
        'pizzas_medianas': pizzas_medianas,
        'pizzas_slice': pizzas_slice,
        'form': form,
    })
