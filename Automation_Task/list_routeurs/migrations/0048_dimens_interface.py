# Generated by Django 3.2.4 on 2021-10-30 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0047_switch_capa'),
    ]

    operations = [
        migrations.AddField(
            model_name='dimens',
            name='interface',
            field=models.CharField(blank=True, max_length=20000, null=True),
        ),
    ]