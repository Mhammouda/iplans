# Generated by Django 3.2.4 on 2021-11-17 10:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0051_auto_20211116_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicemanuel',
            name='interface',
            field=models.CharField(max_length=100, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{2}/[0-9]{2}/[0-9]{2}$', 'le syntaxe doit etre XX/XX/XX')]),
        ),
    ]
