# Generated by Django 3.2.9 on 2022-02-26 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('list_routeurs', '0077_delete_historicalservice'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalService',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('nomClient', models.CharField(default='nom du client', max_length=100, null=True)),
                ('switch', models.CharField(blank=True, max_length=100, null=True)),
                ('interface', models.CharField(blank=True, max_length=100, null=True)),
                ('interfacertsw', models.CharField(blank=True, max_length=100, null=True)),
                ('vlan', models.PositiveIntegerField(max_length=5, null=True)),
                ('debit', models.PositiveIntegerField(blank=True, max_length=5, null=True)),
                ('ipadress', models.CharField(max_length=100, null=True)),
                ('ipadresspublic', models.CharField(blank=True, max_length=100, null=True)),
                ('ipadresspublic31', models.CharField(blank=True, max_length=100, null=True)),
                ('ipadresspublic28', models.CharField(blank=True, max_length=100, null=True)),
                ('ipadresspublic29', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('user', models.CharField(max_length=100, null=True)),
                ('VRF', models.CharField(choices=[('Internet_vpn', 'Internet_vpn')], max_length=100, null=True)),
                ('trans', models.CharField(choices=[('FH', 'FH'), ('FO', 'FO')], max_length=100, null=True)),
                ('generate', models.CharField(blank=True, max_length=100000, null=True)),
                ('etat', models.CharField(blank=True, default='DEMANDE', max_length=100000, null=True)),
                ('swan', models.CharField(blank=True, default='XXXXX', max_length=100000, null=True)),
                ('date_changement', models.DateTimeField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=10000, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('routeur', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='list_routeurs.routeur', to_field='Loopback')),
            ],
            options={
                'verbose_name': 'historical service',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
