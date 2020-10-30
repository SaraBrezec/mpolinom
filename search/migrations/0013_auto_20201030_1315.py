# Generated by Django 3.0.4 on 2020-10-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0012_auto_20201030_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalcomment',
            name='status',
            field=models.CharField(choices=[('waiting', 'waiting'), ('approved', 'approved'), ('declined', 'declined'), ('new_comments', 'new comments')], default='waiting', max_length=15),
        ),
        migrations.AlterField(
            model_name='historicalmpolynom',
            name='status',
            field=models.CharField(choices=[('waiting', 'waiting'), ('approved', 'approved'), ('declined', 'declined'), ('new_comments', 'new comments')], default='waiting', max_length=15),
        ),
        migrations.AlterField(
            model_name='mpolynom',
            name='status',
            field=models.CharField(choices=[('waiting', 'waiting'), ('approved', 'approved'), ('declined', 'declined'), ('new_comments', 'new comments')], default='waiting', max_length=15),
        ),
    ]