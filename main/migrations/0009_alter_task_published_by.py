# Generated by Django 5.1.3 on 2024-11-18 01:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_alter_task_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="published_by",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.coder",
                verbose_name="Автор",
            ),
        ),
    ]