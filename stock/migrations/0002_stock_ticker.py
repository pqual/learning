# Generated by Django 4.1.1 on 2022-09-12 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="ticker",
            field=models.CharField(default="NULL", max_length=4),
        ),
    ]
