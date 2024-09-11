# Generated by Django 5.1 on 2024-09-02 08:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_flatfeespermonth"),
    ]

    operations = [
        migrations.AddField(
            model_name="flatfeespermonth",
            name="monthly_expenses",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.monthlyexpense",
            ),
        ),
    ]
