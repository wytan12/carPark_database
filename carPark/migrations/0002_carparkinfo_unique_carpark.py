# Generated by Django 5.1 on 2024-08-28 01:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("carPark", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="carparkinfo",
            constraint=models.UniqueConstraint(
                fields=("carpark_id", "lot_type"), name="unique_carpark"
            ),
        ),
    ]
