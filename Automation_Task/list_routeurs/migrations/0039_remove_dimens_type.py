# Generated by Django 3.2.4 on 2021-10-09 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0038_dimens_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dimens',
            name='type',
        ),
    ]
