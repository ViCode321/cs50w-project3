from django.urls import path
from . import views
from .views import login_view, logout_view

urlpatterns = [
    path('', views.start, name='start'),  # Asociar la URL raíz a la vista de inicio
    path('menu/', views.index, name='menu'),
    path('register/', views.register_view, name='register'),    
    path('carrito/', views.carrito, name='carrito'),    
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_to_cart/<int:pizza_id>/', views.add_to_cart, name='add_to_cart'),    
    # Otras URLS
]