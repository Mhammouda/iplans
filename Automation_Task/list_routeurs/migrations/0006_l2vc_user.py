# Generated by Django 3.2.4 on 2021-09-15 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0005_service_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='l2vc',
            name='user',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
