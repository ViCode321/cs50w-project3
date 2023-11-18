from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class Pizza(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    toppings = models.ManyToManyField('Topping')
    additional_ingredients = models.ManyToManyField('AdditionalIngredient')
    image_url = models.CharField(max_length=255, default='URL_predeterminada')

    def __str__(self):
        return f"{self.name} - {self.size}"


class Topping(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class AdditionalIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        toppings_list = ', '.join(topping.name for topping in self.pizza.toppings.all())
        ingredients_list = ', '.join(ingredient.name for ingredient in self.pizza.additional_ingredients.all())

        return f"{self.quantity} x {self.pizza.name} ({self.pizza.size}) - Toppings: {toppings_list} - Ingredientes adicionales: {ingredients_list} - Precio por unidad: ${self.pizza.price}"

class OrderItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - Total: ${self.total}"
        