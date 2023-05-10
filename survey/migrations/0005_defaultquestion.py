# Generated by Django 4.2 on 2023-04-19 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_survey_is_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('question_type', models.CharField(max_length=50)),
                ('properties', models.JSONField(default=dict)),
                ('marks', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'DefaultQuestion',
            },
        ),
    ]
