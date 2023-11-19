from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from orders.forms import PizzaForm, CustomUserCreationForm
from orders.models import CartItem, Pizza, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
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
            elif action == 'decrease':
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                else:
                    item.delete()
            elif action == 'increase':
                item.quantity += 1
                item.save()
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
        #messages.success(request, 'Producto eliminado del carrito.')
    else:
        messages.error(request, 'No tienes permisos para realizar esta acción.')

    return redirect('carrito')

@transaction.atomic
def place_order(request):
    if request.method == 'POST':
        user_cart_items = CartItem.objects.filter(user=request.user)

        # Verificar si el carrito está vacío
        if not user_cart_items.exists():
            #messages.error(request, 'Error al colocar la orden. El carrito está vacío.')
            return redirect('carrito')

        # Crear la orden
        for item in user_cart_items:
            OrderItem.objects.create(user=request.user, pizza=item.pizza, quantity=item.quantity, total=item.pizza.price * item.quantity)

        # Limpiar el carrito
        user_cart_items.delete()

        #messages.success(request, 'Orden colocada exitosamente. ¡Gracias por tu compra!')

        # Redirigir a la página de pedidos después de realizar la orden
        return redirect('pedidos')
    
    # Si no es una solicitud POST, mostrar un mensaje de error
    messages.error(request, 'Error al colocar la orden. Intenta nuevamente.')
    return redirect('carrito')

def pedidos(request):
    order_items = OrderItem.objects.filter(user=request.user)
    orders = []
    for order_item in order_items:
        order_details = {
            'order_id': order_item.id,
            'user': order_item.user.username,
            'order_date': order_item.order_date,
            'items': [
                {
                    'pizza_name': order_item.pizza.name,
                    'quantity': order_item.quantity,
                    'size': order_item.pizza.size,
                    'price': order_item.total,
                }
            ]
        }
        orders.append(order_details)
    total_general = sum(order_item.total for order_item in order_items)
    return render(request, 'pedidos.html', {'orders': orders, 'total_general': total_general})

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
        print('Form is valid: ', form.is_valid())
        print('Form errors: ', form.errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('start')
        else:
            messages.error(request, 'Hubo un error en el registro. Corrige los errores a continuación.')
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def is_admin(user):
    return user.is_superuser

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
    
    # Clasifica las pizzas por tamaño
    pizzas_familiares = []
    pizzas_grandes = []
    pizzas_medianas = []
    pizzas_slice = []

    for pizza in pizzas:
        # Convierte el tamaño a un entero antes de comparar
        if float(pizza.size) >= 12:
            pizzas_familiares.append(pizza)
        elif float(pizza.size) >= 8:
            pizzas_grandes.append(pizza)
        elif float(pizza.size) >= 6:
            pizzas_medianas.append(pizza)
        elif float(pizza.size) >= 4:
            pizzas_slice.append(pizza)

    return render(request, 'menu.html', {
        'pizzas_familiares': pizzas_familiares,
        'pizzas_grandes': pizzas_grandes,
        'pizzas_medianas': pizzas_medianas,
        'pizzas_slice': pizzas_slice,
        'form': form,
    })

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import OrderItem  # Asegúrate de importar tu modelo OrderItem
from django.template.loader import render_to_string
from django.conf import settings

def view_orders(request):
    order_items = OrderItem.objects.all()
    orders = []
    total_general = 0

    for order_item in order_items:
        order_details = {
            'order_id': order_item.id,
            'user': order_item.user.username,
            'order_date': order_item.order_date,
            'items': [
                {
                    'pizza_name': order_item.pizza.name,
                    'quantity': order_item.quantity,
                    'size': order_item.pizza.size,
                    'price': order_item.total,
                }
            ]
        }
        orders.append(order_details)
        total_general += order_item.total
    return render(request, 'view_orders.html', {'orders': orders, 'total_general': total_general})

@transaction.atomic
def confirm_order(request, order_id):
    order = get_object_or_404(OrderItem, id=order_id)

    if request.method == 'POST':
        send_order_confirmation_email(order.user, order)
        order.delete()  # Elimina el pedido después de enviar el correo electrónico de confirmación
        return redirect('view_orders')

    messages.error(request, 'Error al confirmar la orden. Intenta nuevamente.')
    return redirect('view_orders')

def send_order_confirmation_email(user, order):
    subject = 'Confirmación de Orden'
    message = 'Su pedido ha sido confirmado y está en proceso.'  # Aquí va tu mensaje de confirmación
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
