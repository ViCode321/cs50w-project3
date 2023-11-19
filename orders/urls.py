from django.urls import path
from . import views
from .views import login_view, logout_view, remove_from_cart, cart_view

urlpatterns = [
    path('', views.start, name='start'),  # Asociar la URL raíz a la vista de inicio
    path('menu/', views.index, name='menu'),
    path('register/', views.register_view, name='register'),    
    path('carrito/', views.carrito, name='carrito'),    
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_to_cart/<int:pizza_id>/', views.add_to_cart, name='add_to_cart'),    
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart_view/', cart_view, name='cart_view'),
    # Otras URLS
]