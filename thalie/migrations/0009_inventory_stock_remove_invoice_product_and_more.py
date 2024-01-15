# Generated by Django 5.0 on 2024-01-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thalie', '0008_invoice_customer_invoice_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='product',
        ),
        migrations.AddField(
            model_name='invoice',
            name='product',
            field=models.ManyToManyField(to='thalie.product'),
        ),
    ]
