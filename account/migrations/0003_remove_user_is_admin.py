# Generated by Django 4.2 on 2023-04-10 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
    ]
