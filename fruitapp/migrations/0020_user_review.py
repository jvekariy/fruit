# Generated by Django 5.1 on 2024-11-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruitapp', '0019_checkout_page_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comments', models.CharField(max_length=50)),
            ],
        ),
    ]
