# Generated by Django 3.2.4 on 2021-10-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0033_alter_trafic_routeur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafic',
            name='percent',
            field=models.FloatField(blank=True, choices=[], null=True),
        ),
    ]
