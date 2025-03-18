from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Transaction, Category, Budget

class UserLoginForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(label="Nazwa użytkownika", 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", 
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserRegisterForm(UserCreationForm):
    """Custom registration form"""
    email = forms.EmailField(label="Email", 
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nazwa użytkownika',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password1'].label = "Hasło"
        self.fields['password2'].label = "Powtórz hasło"

class TransactionForm(forms.ModelForm):
    """Form for adding and editing transactions"""
    
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'title', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'category': 'Kategoria',
            'amount': 'Kwota',
            'title': 'Tytuł',
            'description': 'Opis',
            'date': 'Data',
        }

class CategoryForm(forms.ModelForm):
    """Form for adding and editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'icon', 'is_expense']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'is_expense': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nazwa',
            'icon': 'Ikona',
            'is_expense': 'Czy wydatek',
        }

class BudgetForm(forms.ModelForm):
    """Form for setting budget limits"""
    
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'period_start', 'period_end']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'period_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'period_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'category': 'Kategoria',
            'amount': 'Limit',
            'period_start': 'Początek okresu',
            'period_end': 'Koniec okresu',
        }

class DateRangeForm(forms.Form):
    """Form for filtering transactions by date range"""
    start_date = forms.DateField(
        label="Data początkowa",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label="Data końcowa",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )