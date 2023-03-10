# Generated by Django 3.0 on 2023-02-23 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Order'), ('0', 'Not_order')], default='0', max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.cart')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Users')),
            ],
        ),
    ]
