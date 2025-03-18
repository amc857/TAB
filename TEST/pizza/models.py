from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model for the budget application"""
    
    class Meta:
        verbose_name = "U¿ytkownik"
        verbose_name_plural = "U¿ytkownicy"

    def __str__(self):
        return self.username

class Category(models.Model):
    """Categories for income and expenses"""
    name = models.CharField("Nazwa", max_length=50)
    icon = models.CharField("Ikona", max_length=50, blank=True)
    is_expense = models.BooleanField("Czy wydatek", default=True)
    
    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Model for all financial transactions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField("Kwota", max_digits=10, decimal_places=2)
    title = models.CharField("Tytu³", max_length=100)
    description = models.TextField("Opis", blank=True)
    date = models.DateField("Data", default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Transakcja"
        verbose_name_plural = "Transakcje"
        ordering = ["-date", "-created_at"]
    
    def __str__(self):
        return f"{self.title} ({self.amount} z³)"
    
    @property
    def is_expense(self):
        return self.category.is_expense

class Budget(models.Model):
    """Budget limits for specific categories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")
    amount = models.DecimalField("Limit", max_digits=10, decimal_places=2)
    period_start = models.DateField("Pocz¹tek okresu")
    period_end = models.DateField("Koniec okresu")
    
    class Meta:
        verbose_name = "Bud¿et"
        verbose_name_plural = "Bud¿ety"
        
    def __str__(self):
        return f"Bud¿et dla {self.category.name}: {self.amount} z³"
    
    def get_spent_amount(self):
        """Calculate how much has been spent in this budget category"""
        return Transaction.objects.filter(
            user=self.user,
            category=self.category,
            date__gte=self.period_start,
            date__lte=self.period_end
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    def get_remaining(self):
        """Calculate remaining budget"""
        return self.amount - self.get_spent_amount()