from django.urls import path

from . import views

app_name = "pizza"

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login, name="login"),
    path("menu/", views.menu, name="menu"),
]