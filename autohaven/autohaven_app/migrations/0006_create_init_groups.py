from django.db import migrations
from django.contrib.auth.models import Group


def create_initial_groups(apps, schema_editor):

    Group = apps.get_model('auth', 'Group')

    # Create groups
    Group.objects.get_or_create(name='SuperUsers')
    Group.objects.get_or_create(name='Sellers')
    Group.objects.get_or_create(name='RegularUsers')


class Migration(migrations.Migration):

    dependencies = [
        ('autohaven_app', '0005_alter_listingmodel_description'),  # Adjust the dependency if necessary
    ]

    operations = [
        migrations.RunPython(create_initial_groups),
    ]
