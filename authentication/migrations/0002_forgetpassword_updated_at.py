# Generated by Django 4.2 on 2023-04-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forgetpassword',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
