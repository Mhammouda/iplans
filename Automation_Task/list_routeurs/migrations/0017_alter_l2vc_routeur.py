# Generated by Django 3.2.4 on 2021-09-24 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0016_l2vc_switch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='l2vc',
            name='routeur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='list_routeurs.routeur', to_field='Loopback'),
        ),
    ]