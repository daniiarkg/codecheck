# Generated by Django 5.1.3 on 2024-11-27 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0015_rename_coder_taskcomplete_solved_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskcomplete",
            name="solved_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.coder",
            ),
        ),
        migrations.AlterField(
            model_name="taskcomplete",
            name="task",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="main.task"
            ),
        ),
    ]