# Generated by Django 3.0.3 on 2020-02-11 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
