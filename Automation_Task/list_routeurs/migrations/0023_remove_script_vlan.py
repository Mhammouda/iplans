# Generated by Django 3.2.4 on 2021-09-26 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0022_alter_script_interface'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='script',
            name='vlan',
        ),
    ]
