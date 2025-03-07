from django import forms

from .models import User, Food


class UserLoginForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["mail", "password"]
        labels = {
            "mail": "Email",
            "password": "Hasło"
        }

class UserRegisterForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("name","second_name","mail","password")
        labels = {
            "name": "Imię",
            "second_name": "Nazwisko",
            "mail": "Email",
            "password": "Hasło"
        }

class FoodForm(forms.ModelForm):
    
    class Meta:
        model = Food
        fields = ("name", "price", "img", "opis")
        labels = {
            "name": "Nazwa",
            "price": "Cena",
            "img": "Img",
            "opis": "Opis"
        }


