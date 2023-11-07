from django.db import models
from django.contrib.auth.models import AbstractUser

class Pizza(models.Model):
    """
    Representa una pizza.

    Attributes:
        name: El nombre de la pizza.
        size: El tamaño de la pizza.
        price: El precio de la pizza.
        toppings: Las coberturas de la pizza.
        additional_ingredients: Los ingredientes adicionales de la pizza.
        image: La imagen de la pizza.
    """
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
        name: El nombre de la cobertura.
        price: El precio de la cobertura.
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class AdditionalIngredient(models.Model):
    """
    Representa un ingrediente adicional para pizza.

    Attributes:
        name: El nombre del ingrediente adicional.
        price: El precio del ingrediente adicional.
    """

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

#################################################################
class CustomUser(AbstractUser):
    # Campos personalizados, como first_name, last_name y email
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
