# Generated by Django 2.1.5 on 2019-01-11 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('account', '0001_initial'),
        ('source', '0001_initial'),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Foresight',
            new_name='DirectDebit',
        ),
        migrations.AlterModelOptions(
            name='directdebit',
            options={'base_manager_name': 'objects', 'verbose_name': 'direct debit', 'verbose_name_plural': 'direct debits'},
        ),
    ]
