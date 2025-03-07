from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(("Imie"), max_length=50)
    second_name = models.CharField(("Nazwisko"), max_length=50)
    mail = models.EmailField(("Email"), max_length=254)
    password = models.CharField(("Haslo"), max_length=50)
    is_admin = models.BooleanField(("isAdmin"))

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})

class Food(models.Model):

    name = models.CharField(("Nazwa"), max_length=50)
    price = models.FloatField(("Cena"))
    img = models.URLField(("Zdjecie"))
    opis = models.CharField(("Opis"), max_length=100)


    class Meta:
        verbose_name = ("Food")
        verbose_name_plural = ("Foods")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Food_detail", kwargs={"pk": self.pk})
