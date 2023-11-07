from django import forms
from .models import Pizza

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'size', 'price', 'toppings', 'additional_ingredients', 'image_url']
