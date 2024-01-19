# Generated by Django 3.2.4 on 2021-10-08 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0034_alter_trafic_percent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dimens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liaison', models.CharField(max_length=100, null=True)),
                ('percent', models.FloatField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]