from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UserLoginForm, FoodForm
from .models import User, Food


# Create your views here.
def index(request):
    user = request.session['username'] if 'username' in request.session else None
    form = None
    context = {}
    context["user"]=user
    return render(request,"pizza/index.html", context)

def login(request):
    user = None
    context = {}
    context['errors'] = None
    context['user']=user
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if 'password' in request.POST and 'mail' in request.POST:
            temp = User.objects.filter(mail=request.POST['mail'],password=request.POST['password'])
            if len(temp) > 0:
                #Zgadza się
                user = temp[0]
                request.session['username']=user.name
                context['user']=user
                return render(request, "pizza/index.html", context)
            else:
                #Błędne dane
                context['errors'] = 'Błędne dane'
        
        else:
            #temp cały post do wyświetlenia
            user = request.POST 
            context["user"]=user
    
    
    context["form"]=form
    return render(request, "pizza/login.html", context)

def menu(request):
    user = request.session['username'] if 'username' in request.session else None
    form = FoodForm()
    context = {}
    context["user"]=user
    menu = Food.objects.all()
    context['menu']=menu
    return render(request,"pizza/menu.html", context)