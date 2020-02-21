# Generated by Django 3.0.3 on 2020-02-21 14:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20200221_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskgroup',
            name='credate',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='taskgroup',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
