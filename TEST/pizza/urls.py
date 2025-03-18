from django.urls import path
from . import views

app_name = "budget"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    
    # Transaction URLs
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("transactions/add/", views.transaction_create, name="transaction_create"),
    path("transactions/<int:pk>/edit/", views.transaction_edit, name="transaction_edit"),
    path("transactions/<int:pk>/delete/", views.transaction_delete, name="transaction_delete"),
    
    # Category URLs
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_create"),
    
    # Budget URLs
    path("budgets/", views.budget_list, name="budget_list"),
    path("budgets/add/", views.budget_create, name="budget_create"),
    
    # Reports
    path("reports/", views.reports, name="reports"),
]