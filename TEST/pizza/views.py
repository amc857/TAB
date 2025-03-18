from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Case, When, DecimalField, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import datetime, timedelta

from .models import User, Transaction, Category, Budget
from .forms import UserLoginForm, UserRegisterForm, TransactionForm, CategoryForm, BudgetForm, DateRangeForm

def index(request):
    """Home page view"""
    context = {}
    if request.user.is_authenticated:
        # Get summary for the current month
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        
        # Get income and expenses for the current month
        income_sum = Transaction.objects.filter(
            user=request.user,
            category__is_expense=False,
            date__gte=start_of_month,
            date__lte=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        expense_sum = Transaction.objects.filter(
            user=request.user,
            category__is_expense=True,
            date__gte=start_of_month,
            date__lte=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Get recent transactions
        recent_transactions = Transaction.objects.filter(
            user=request.user
        ).order_by('-date', '-created_at')[:5]
        
        # Get budget summary
        budgets = Budget.objects.filter(
            user=request.user,
            period_start__lte=today,
            period_end__gte=today
        )
        
        context = {
            'income_sum': income_sum,
            'expense_sum': expense_sum,
            'balance': income_sum - expense_sum,
            'recent_transactions': recent_transactions,
            'budgets': budgets,
        }
    return render(request, "budget/index.html", context)

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('budget:index')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Rejestracja przebiegła pomyślnie!")
            return redirect('budget:index')
    else:
        form = UserRegisterForm()
    
    return render(request, "budget/register.html", {'form': form})

def login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('budget:index')
        
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Zalogowano pomyślnie!")
            return redirect('budget:index')
    else:
        form = UserLoginForm()
    
    return render(request, "budget/login.html", {'form': form})

@login_required
def logout(request):
    """User logout view"""
    auth_logout(request)
    messages.success(request, "Wylogowano pomyślnie!")
    return redirect('budget:index')

@login_required
def transaction_list(request):
    """List all transactions with filtering options"""
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')
    
    date_range_form = DateRangeForm(request.GET or None)
    if date_range_form.is_valid():
        start_date = date_range_form.cleaned_data['start_date']
        end_date = date_range_form.cleaned_data['end_date']
        transactions = transactions.filter(date__gte=start_date, date__lte=end_date)
    
    return render(request, "budget/transaction_list.html", {
        'transactions': transactions,
        'date_range_form': date_range_form
    })

@login_required
def transaction_create(request):
    """Create a new transaction"""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transakcja została dodana!")
            return redirect('budget:transaction_list')
    else:
        form = TransactionForm()
    
    return render(request, "budget/transaction_form.html", {'form': form, 'is_new': True})

@login_required
def transaction_edit(request, pk):
    """Edit an existing transaction"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transakcja została zaktualizowana!")
            return redirect('budget:transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, "budget/transaction_form.html", {'form': form, 'is_new': False})

@login_required
def transaction_delete(request, pk):
    """Delete a transaction"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transakcja została usunięta!")
        return redirect('budget:transaction_list')
    
    return render(request, "budget/transaction_confirm_delete.html", {'transaction': transaction})

@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    return render(request, "budget/category_list.html", {'categories': categories})

@login_required
def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoria została dodana!")
            return redirect('budget:category_list')
    else:
        form = CategoryForm()
    
    return render(request, "budget/category_form.html", {'form': form, 'is_new': True})

@login_required
def budget_list(request):
    """List all budgets"""
    budgets = Budget.objects.filter(user=request.user)
    return render(request, "budget/budget_list.html", {'budgets': budgets})

@login_required
def budget_create(request):
    """Create a new budget"""
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budżet został dodany!")
            return redirect('budget:budget_list')
    else:
        form = BudgetForm()
    
    return render(request, "budget/budget_form.html", {'form': form, 'is_new': True})

@login_required
def reports(request):
    """Generate reports and statistics"""
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    
    # Default to current month
    start_date = start_of_month
    end_date = today
    
    # Process date range form if submitted
    date_range_form = DateRangeForm(request.GET or None)
    if date_range_form.is_valid():
        start_date = date_range_form.cleaned_data['start_date']
        end_date = date_range_form.cleaned_data['end_date']
    
    # Get category-wise expenses
    expense_by_category = Transaction.objects.filter(
        user=request.user,
        category__is_expense=True,
        date__gte=start_date,
        date__lte=end_date
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Get category-wise income
    income_by_category = Transaction.objects.filter(
        user=request.user,
        category__is_expense=False,
        date__gte=start_date,
        date__lte=end_date
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Get daily expenses for the selected period
    daily_transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).values('date').annotate(
        expenses=Sum(Case(
            When(category__is_expense=True, then=F('amount')),
            default=Value(0),
            output_field=DecimalField()
        )),
        income=Sum(Case(
            When(category__is_expense=False, then=F('amount')),
            default=Value(0),
            output_field=DecimalField()
        ))
    ).order_by('date')
    
    # Total summary
    total_income = Transaction.objects.filter(
        user=request.user,
        category__is_expense=False,
        date__gte=start_date,
        date__lte=end_date
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = Transaction.objects.filter(
        user=request.user,
        category__is_expense=True,
        date__gte=start_date,
        date__lte=end_date
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'expense_by_category': expense_by_category,
        'income_by_category': income_by_category,
        'daily_transactions': daily_transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': total_income - total_expenses,
        'date_range_form': date_range_form,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, "budget/reports.html", context)