# Generated by Django 5.0.6 on 2024-07-11 11:20

from django.db import migrations
from django.contrib.auth import get_user_model

def create_more_users(apps, schema_editor):
    
    User = get_user_model()
    Group = apps.get_model('auth', 'Group')

    group_name3 = "RegularUsers"  
    regularuser_group = Group.objects.get(name=group_name3)

    # Create a new regular user
    regular_user, created = User.objects.get_or_create(
        username='bediuser',
        defaults={
            'first_name': 'Bedi',
            'last_name': 'DummyUser',
            'email': 'bediuser@firefox.com',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        regular_user.set_password('bedipassword')
        regular_user.save()
        regular_user.groups.add(regularuser_group.id)

    # Create a new regular user
    regular_user, created = User.objects.get_or_create(
        username='berfinuser',
        defaults={
            'first_name': 'Berfin',
            'last_name': 'DummyUser',
            'email': 'berfinuser@firefox.com',
            'is_staff': False,
            'is_superuser': False
        }
    )
    if created:
        regular_user.set_password('berfinpassword')
        regular_user.save()
        regular_user.groups.add(regularuser_group.id)


class Migration(migrations.Migration):
    dependencies = [
        ("autohaven_app", "0007_create_init_users"),
    ]

    operations = [migrations.RunPython(create_more_users),
    ]
