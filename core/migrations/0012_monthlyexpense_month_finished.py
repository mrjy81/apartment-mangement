# Generated by Django 5.1 on 2024-09-02 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_monthlyexpense_sum_of_expenses"),
    ]

    operations = [
        migrations.AddField(
            model_name="monthlyexpense",
            name="month_finished",
            field=models.BooleanField(default=False),
        ),
    ]
