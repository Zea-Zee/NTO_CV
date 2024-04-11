# Generated by Django 4.2 on 2024-04-10 07:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Image",
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
                ("name", models.CharField(max_length=100)),
                ("image", models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name="Places",
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
                ("XID", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("OSM", models.CharField(max_length=100)),
                ("Longitude", models.FloatField()),
                ("Lat", models.FloatField()),
                ("category", models.ManyToManyField(to="server.category")),
            ],
        ),
    ]