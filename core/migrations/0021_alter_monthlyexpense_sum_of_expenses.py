# Generated by Django 5.1 on 2024-09-02 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_flatfeespermonth_is_paid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monthlyexpense",
            name="sum_of_expenses",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]