# Generated by Django 3.0 on 2023-02-23 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_name',
            new_name='productname',
        ),
    ]