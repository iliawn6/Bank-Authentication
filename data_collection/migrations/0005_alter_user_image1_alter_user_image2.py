# Generated by Django 4.2.6 on 2023-10-18 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_collection", "0004_alter_user_image1_alter_user_image2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image1",
            field=models.ImageField(upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="user",
            name="image2",
            field=models.ImageField(upload_to="images/"),
        ),
    ]
