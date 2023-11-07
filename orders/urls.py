from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),  # Asociar la URL raíz a la vista de inicio
    path('menu/', views.index, name='menu'),
    path('register/', views.register_view, name='register'),    
    path('login/', views.login_view, name='login'),
    # Otras URLS
]