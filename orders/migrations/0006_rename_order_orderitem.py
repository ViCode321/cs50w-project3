# Generated by Django 4.0 on 2023-11-18 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_rename_created_at_order_order_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='OrderItem',
        ),
    ]
