from django.contrib import admin
from .models import Food, User

# Register your models here.
admin.site.register(User)
admin.site.register(Food)