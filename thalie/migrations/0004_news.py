# Generated by Django 5.0 on 2024-01-02 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thalie', '0003_inventory_subtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]