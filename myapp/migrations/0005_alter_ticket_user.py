# Generated by Django 5.0.4 on 2025-01-18 12:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_customuser_last_activity_alter_addnewemployee_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to=settings.AUTH_USER_MODEL),
        ),
    ]
