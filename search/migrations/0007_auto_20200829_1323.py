# Generated by Django 3.0.4 on 2020-08-29 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_auto_20200829_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpolynom',
            name='status',
            field=models.CharField(choices=[('waiting', 'waiting'), ('approved', 'approved'), ('disapproved', 'disapproved')], default='waiting', max_length=15),
        ),
    ]
