# Generated by Django 4.1.6 on 2023-02-08 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_manager', '0002_alter_user_league'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(null=True, verbose_name='Numer telefonu'),
        ),
    ]
