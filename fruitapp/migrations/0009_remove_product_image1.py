# Generated by Django 5.1 on 2024-09-27 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fruitapp', '0008_product_image1_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image1',
        ),
    ]
