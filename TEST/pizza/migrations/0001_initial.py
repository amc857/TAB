# Generated by Django 4.2.11 on 2025-02-01 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nazwa')),
                ('price', models.FloatField(verbose_name='Cena')),
                ('img', models.ImageField(upload_to=None, verbose_name='Zdjecie')),
                ('opis', models.CharField(max_length=100, verbose_name='Opis')),
            ],
            options={
                'verbose_name': 'Food',
                'verbose_name_plural': 'Foods',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Imie')),
                ('second_name', models.CharField(max_length=50, verbose_name='Nazwisko')),
                ('mail', models.EmailField(max_length=254, verbose_name='Email')),
                ('password', models.CharField(max_length=50, verbose_name='Haslo')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
