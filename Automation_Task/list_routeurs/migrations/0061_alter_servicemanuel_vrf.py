# Generated by Django 3.2.4 on 2021-11-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_routeurs', '0060_l2vc_interfacertsw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicemanuel',
            name='VRF',
            field=models.CharField(choices=[('Internet_vpn', 'Internet_vpn'), ('Boutique_Orange', 'Boutique_Orange'), ('Voice_vpn', 'Voice_vpn'), ('CCTV_Wimax', 'CCTV_Wimax'), ('CCTV', 'CCTV'), ('MonitoringB2B_vpn', 'MonitoringB2B_vpn')], max_length=100, null=True),
        ),
    ]
