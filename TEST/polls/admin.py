from django.contrib import admin
from .models import User, Category, Transaction, Budget

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_expense')
    list_filter = ('is_expense',)
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'amount', 'date')
    list_filter = ('category', 'date', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'period_start', 'period_end')
    list_filter = ('category', 'user')
    search_fields = ('user__username', 'category__name')