# Generated by Django 3.2.4 on 2021-10-04 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0027_alter_service_switch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='l2vc',
            name='switch',
            field=models.CharField(blank=True, choices=[], max_length=100, null=True),
        ),
    ]
