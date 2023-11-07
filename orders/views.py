from django.http import HttpResponse
from django.shortcuts import redirect, render
from orders.forms import PizzaForm
from orders.models import Pizza
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


def start(request):
    return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pagina_de_inicio')  # Redirige a la página principal después del inicio de sesión
        else:
            # Muestra un mensaje de error en caso de credenciales incorrectas
            error_message = "Nombre de usuario o contraseña incorrectos"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        # Procesar el formulario de registro
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('menu')
    else:
        # Mostrar el formulario vacío
        form = UserCreationForm()    
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