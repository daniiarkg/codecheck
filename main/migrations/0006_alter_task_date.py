# Generated by Django 5.1.3 on 2024-11-18 01:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_coder_user_alter_task_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 11, 18, 1, 32, 44, 507904, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Создано",
            ),
        ),
    ]