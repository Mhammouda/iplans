# Generated by Django 3.2.4 on 2021-10-09 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0039_remove_dimens_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimens',
            name='loopback_dim',
            field=models.CharField(max_length=20000, null=True),
        ),
    ]
