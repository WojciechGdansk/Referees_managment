# Generated by Django 4.1.6 on 2023-02-15 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User_manager', '0001_initial'),
        ('Test_manager', '0001_initial'),
        ('Organization_test', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usertestresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersolving',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_from_test', to='Test_manager.questiontest'),
        ),
        migrations.AddField(
            model_name='usersolving',
            name='test_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Test_manager.alltest'),
        ),
        migrations.AddField(
            model_name='usersolving',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organisetest',
            name='test_for_league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User_manager.league'),
        ),
        migrations.AddField(
            model_name='organisetest',
            name='test_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Test_manager.alltest'),
        ),
    ]