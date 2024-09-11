# Generated by Django 5.1 on 2024-09-01 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_flat_apartment"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("phone", models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="flat",
            name="users",
            field=models.ManyToManyField(to="core.user"),
        ),
    ]