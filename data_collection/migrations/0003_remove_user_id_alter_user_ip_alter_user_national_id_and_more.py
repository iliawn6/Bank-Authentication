# Generated by Django 4.2.6 on 2023-10-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_collection", "0002_user_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="id",
        ),
        migrations.AlterField(
            model_name="user",
            name="ip",
            field=models.CharField(default="127.0.0.1", max_length=20),
        ),
        migrations.AlterField(
            model_name="user",
            name="national_id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="state",
            field=models.CharField(default="pending", max_length=255),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(default="user", max_length=255),
        ),
    ]
