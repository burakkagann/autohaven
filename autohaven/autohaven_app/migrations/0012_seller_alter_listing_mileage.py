# Generated by Django 4.1 on 2024-07-16 22:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("autohaven_app", "0011_create_initial_offer"),
    ]

    operations = [
        migrations.CreateModel(
            name="Seller",
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
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("company_name", models.CharField(max_length=100)),
                ("email_address", models.EmailField(max_length=254)),
                ("username", models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name="listing",
            name="mileage",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
