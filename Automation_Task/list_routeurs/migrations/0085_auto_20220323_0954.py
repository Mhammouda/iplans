# Generated by Django 3.2.9 on 2022-03-23 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0084_auto_20220323_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalservice',
            name='generate',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='generate',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
    ]
