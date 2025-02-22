# Generated by Django 5.0.6 on 2024-07-17 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autohaven_app', "0010_create_intial_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='mileage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=10),
        ),
    ]
