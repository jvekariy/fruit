# Generated by Django 4.2 on 2024-12-28 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fruitapp', '0023_alter_coupon_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout_page',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fruitapp.register'),
        ),
    ]
