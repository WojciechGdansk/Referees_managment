# Generated by Django 4.1.6 on 2023-02-15 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Test_manager', '0001_initial'),
        ('Organization_test', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertestresult',
            name='test_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Test_manager.alltest'),
        ),
    ]
