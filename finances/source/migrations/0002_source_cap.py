# Generated by Django 2.1.5 on 2019-01-11 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='cap',
            field=models.PositiveSmallIntegerField(default=0, help_text='monthly spending cap', verbose_name='spending cap'),
        ),
    ]
