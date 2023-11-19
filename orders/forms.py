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

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

