# Generated by Django 3.2.9 on 2022-02-18 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0067_service_range_adress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='range_adress',
        ),
    ]
