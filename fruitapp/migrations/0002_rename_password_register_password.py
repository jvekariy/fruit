# Generated by Django 5.1 on 2024-09-10 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fruitapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='Password',
            new_name='password',
        ),
    ]
