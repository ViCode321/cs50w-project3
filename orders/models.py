from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class Pizza(models.Model):
    """
    Representa una pizza.

    Attributes:
        id: Campo explícito de clave primaria.
        name: El nombre de la pizza.
        size: El tamaño de la pizza.
        price: El precio de la pizza.
        toppings: Las coberturas de la pizza.
        additional_ingredients: Los ingredientes adicionales de la pizza.
        image: La imagen de la pizza.
    """
    id = models.AutoField(primary_key=True)  # Agrega un campo id explícito
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    toppings = models.ManyToManyField('Topping')
    additional_ingredients = models.ManyToManyField('AdditionalIngredient')
    image_url = models.CharField(max_length=255, default='URL_predeterminada')

class Topping(models.Model):
    """
    Representa una cobertura para pizza.

    Attributes:
        id: Campo explícito de clave primaria.
        name: El nombre de la cobertura.
        price: El precio de la cobertura.
    """
    id = models.AutoField(primary_key=True)  # Agrega un campo id explícito
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class AdditionalIngredient(models.Model):
    """
    Representa un ingrediente adicional para pizza.

    Attributes:
        id: Campo explícito de clave primaria.
        name: El nombre del ingrediente adicional.
        price: El precio del ingrediente adicional.
    """
    id = models.AutoField(primary_key=True)  # Agrega un campo id explícito
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


#################################################################
class CustomUser(AbstractUser):
    # Campos personalizados, como first_name, last_name y email
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    #url = models.ImageField Para imagen

class CartItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.pizza.name} ({self.user.username})"