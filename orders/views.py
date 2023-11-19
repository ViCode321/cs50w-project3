from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from orders.forms import PizzaForm
from orders.models import CartItem, Pizza
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm

def start(request):
    return render(request, 'index.html')

def carrito(request):
    user_cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        item = get_object_or_404(CartItem, id=item_id)

        if item.user == request.user:
            if action == 'remove':
                item.delete()
                messages.success(request, 'Producto eliminado del carrito.')
            elif action == 'decrease':
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                    messages.success(request, 'Cantidad reducida en 1.')
                else:
                    item.delete()
                    messages.success(request, 'Producto eliminado del carrito.')
            elif action == 'increase':
                item.quantity += 1
                item.save()
                messages.success(request, 'Cantidad aumentada en 1.')
        else:
            messages.error(request, 'No tienes permisos para realizar esta acción.')

        return redirect('carrito')

    context = {
        'cart_items': user_cart_items,
    }

    return render(request, 'carrito.html', context)

def add_to_cart(request, pizza_id):
    pizza = get_object_or_404(Pizza, pk=pizza_id)

    # Verificar si ya existe un elemento en el carrito para esta pizza y usuario
    existing_cart_item = CartItem.objects.filter(user=request.user, pizza=pizza).first()

    if existing_cart_item:
        # Si ya existe, aumentar la cantidad
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        # Si no existe, crear un nuevo elemento en el carrito
        CartItem.objects.create(user=request.user, pizza=pizza, quantity=1)

    return redirect('menu') 

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.user == request.user:
        item.delete()
        messages.success(request, 'Producto eliminado del carrito.')
    else:
        messages.error(request, 'No tienes permisos para realizar esta acción.')

    return redirect('carrito')

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

def cart_view(request):
    user_cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST' and request.is_ajax():
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        item = get_object_or_404(CartItem, id=item_id)

        if item.user == request.user:
            if action == 'remove':
                item.delete()
                messages.success(request, 'Producto eliminado del carrito.')
            elif action == 'decrease':
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                    messages.success(request, 'Cantidad reducida en 1.')
                else:
                    item.delete()
                    messages.success(request, 'Producto eliminado del carrito.')
            elif action == 'increase':
                item.quantity += 1
                item.save()
                messages.success(request, 'Cantidad aumentada en 1.')

            # Devuelve la información actualizada del carrito en formato JSON
            cart_items = [{'id': item.id, 'name': item.pizza.name, 'size': item.pizza.size, 'price': item.pizza.price, 'quantity': item.quantity, 'image_url': item.pizza.image_url} for item in user_cart_items]
            total = sum(item.pizza.price * item.quantity for item in user_cart_items)
            
            response_data = {
                'message': 'Operación exitosa',
                'cart_items': cart_items,
                'total': total,
            }

            return JsonResponse(response_data)
        else:
            messages.error(request, 'No tienes permisos para realizar esta acción.')

    context = {
        'cart_items': user_cart_items,
    }

    return render(request, 'carrito.html', context)
