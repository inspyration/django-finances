# Generated by Django 2.1.5 on 2019-01-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='amount',
        ),
        migrations.AddField(
            model_name='account',
            name='cap',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='spending cap'),
        ),
    ]