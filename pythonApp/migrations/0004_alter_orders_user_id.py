# Generated by Django 4.2 on 2024-01-01 04:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pythonApp', '0003_orders_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
