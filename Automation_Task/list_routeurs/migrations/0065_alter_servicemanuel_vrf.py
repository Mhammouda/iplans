# Generated by Django 3.2.9 on 2021-12-22 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0064_link_node'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicemanuel',
            name='VRF',
            field=models.CharField(choices=[('Internet_vpn', 'Internet_vpn'), ('Boutique_Orange', 'Boutique_Orange'), ('Voice_vpn', 'Voice_vpn'), ('CCTV_Wimax', 'CCTV_Wimax'), ('CCTV', 'CCTV'), ('MonitoringB2B_vpn', 'MonitoringB2B_vpn'), ('Voice_Avaya_Client', 'Voice_Avaya_Client')], max_length=100, null=True),
        ),
    ]
