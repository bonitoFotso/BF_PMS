# Generated by Django 4.2.1 on 2023-08-01 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ressource', '0005_stateday_delete_ajax'),
        ('clients', '0001_initial'),
        ('project', '0008_rapport'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTechnicienTache',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('tache', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project.tache')),
                ('technicien', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='ressource.technicien', verbose_name='techniciens')),
            ],
            options={
                'verbose_name': 'historical technicien tache',
                'verbose_name_plural': 'historical technicien taches',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTache',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, verbose_name='name')),
                ('priorite', models.CharField(choices=[('Bas', 'Bas'), ('Moyen', 'Moyen'), ('Elever', 'Elever')], max_length=20)),
                ('description', models.CharField(default='description', max_length=500)),
                ('n_OS', models.CharField(blank=True, max_length=50, null=True, verbose_name='numero d OS')),
                ('observation', models.CharField(default='observation', max_length=100)),
                ('date_debut', models.DateField(blank=True, null=True, verbose_name='date de debut')),
                ('date_fin', models.DateField(blank=True, null=True, verbose_name='date de fin')),
                ('createdAt', models.DateTimeField(blank=True, editable=False)),
                ('updatedAt', models.DateTimeField(blank=True, editable=False)),
                ('ok', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('appelant', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='clients.appelant', verbose_name=' celui qui appel ')),
                ('etat', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project.etat', verbose_name='etat')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Tache',
                'verbose_name_plural': 'historical Taches',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalRapport',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('corp', models.TextField(verbose_name='rapport')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('techtache', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project.technicientache')),
            ],
            options={
                'verbose_name': 'historical rapport',
                'verbose_name_plural': 'historical rapports',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEtat',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('nom', models.CharField(choices=[('En atente', 'En atente'), ('En cours', 'En cours'), ('En arret', 'En arret'), ('En facturation', 'En facturation')], max_length=20, verbose_name="nom de l'etat")),
                ('description', models.CharField(max_length=50, verbose_name="des criprion de l'etat")),
                ('motif', models.CharField(default='RAS', max_length=50, verbose_name="motif de l'etat")),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical etat',
                'verbose_name_plural': 'historical etats',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]