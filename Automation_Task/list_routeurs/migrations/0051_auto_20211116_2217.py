# Generated by Django 3.2.4 on 2021-11-16 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0050_servicemanuel'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicemanuel',
            name='generate',
            field=models.CharField(max_length=100000, null=True),
        ),
        migrations.AddField(
            model_name='servicemanuel',
            name='user',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
