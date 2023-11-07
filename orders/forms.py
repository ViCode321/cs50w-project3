from django import forms
from .models import Pizza
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'size', 'price', 'toppings', 'additional_ingredients', 'image_url']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
