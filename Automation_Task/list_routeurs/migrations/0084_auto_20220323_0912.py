# Generated by Django 3.2.9 on 2022-03-23 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0083_rename_name_service_reportingb2bservice_name_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalservice',
            name='generate',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='generate',
            field=models.CharField(blank=True, max_length=100000, null=True),
        ),
    ]