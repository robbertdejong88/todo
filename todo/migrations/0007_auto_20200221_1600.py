# Generated by Django 3.0.3 on 2020-02-21 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20200221_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskgroup',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]