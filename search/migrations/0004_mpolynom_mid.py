# Generated by Django 3.0.4 on 2020-06-17 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_mpolynom_nb_tokens'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpolynom',
            name='Mid',
            field=models.CharField(default='5cYDKI3K', max_length=10, verbose_name='id'),
        ),
    ]