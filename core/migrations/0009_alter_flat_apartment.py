# Generated by Django 5.1 on 2024-09-01 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_expensesprice_description_expensesprice_for_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flat",
            name="apartment",
            field=models.ForeignKey(
                default="عباس زاده",
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.apartment",
            ),
        ),
    ]
