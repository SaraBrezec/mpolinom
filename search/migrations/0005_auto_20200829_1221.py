# Generated by Django 3.0.4 on 2020-08-29 10:21

import django.contrib.auth.models
from django.db import migrations, models
import search.models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_mpolynom_mid'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpolynom',
            name='status',
            field=models.CharField(default='waiting', max_length=15),
        ),
        migrations.AlterField(
            model_name='mpolynom',
            name='Mid',
            field=models.CharField(default=search.models.unique_rand, editable=False, max_length=10, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='mpolynom',
            name='author',
            field=models.CharField(default=django.contrib.auth.models.User, editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='mpolynom',
            name='nb_tokens',
            field=models.PositiveSmallIntegerField(default=0, editable=False),
        ),
    ]