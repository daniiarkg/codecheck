# Generated by Django 5.1.3 on 2024-11-18 01:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0011_alter_task_published_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="published_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.coder",
                verbose_name="Автор",
            ),
        ),
    ]