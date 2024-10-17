# Generated by Django 5.1 on 2024-10-14 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruitapp', '0012_wishlist_add_product_wishlist_add_register'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
    ]