# Generated by Django 3.0.3 on 2020-02-21 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20200221_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskgroup',
            name='name',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
    ]