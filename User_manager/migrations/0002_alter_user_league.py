# Generated by Django 4.1.6 on 2023-02-08 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='User_manager.league'),
        ),
    ]
