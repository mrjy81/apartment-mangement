# Generated by Django 5.1 on 2024-09-02 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_apartment_total_population"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expensesprice",
            name="price",
            field=models.FloatField(),
        ),
    ]
