# Generated by Django 3.2.4 on 2021-09-18 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0013_auto_20210918_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='nbraddpriv',
        ),
        migrations.RemoveField(
            model_name='service',
            name='nbraddpub31',
        ),
        migrations.RemoveField(
            model_name='service',
            name='nbraddpub32',
        ),
    ]