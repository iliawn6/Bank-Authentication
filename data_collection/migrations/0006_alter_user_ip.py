# Generated by Django 4.2.6 on 2023-10-18 09:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_collection", "0005_alter_user_image1_alter_user_image2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="ip",
            field=models.CharField(default="local_host", max_length=20),
        ),
    ]
