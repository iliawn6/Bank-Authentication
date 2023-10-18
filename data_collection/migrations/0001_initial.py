# Generated by Django 4.2.6 on 2023-10-17 11:06

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

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
                ("email", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("national_id", models.IntegerField()),
                ("ip", models.CharField(max_length=20)),
                ("image1", models.CharField(max_length=255)),
                ("image2", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
            ],
        ),
    ]
