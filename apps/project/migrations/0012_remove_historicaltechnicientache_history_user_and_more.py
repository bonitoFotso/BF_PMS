# Generated by Django 4.2.1 on 2023-08-01 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_delete_historicalrapport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltechnicientache',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltechnicientache',
            name='tache',
        ),
        migrations.RemoveField(
            model_name='historicaltechnicientache',
            name='technicien',
        ),
        migrations.RemoveField(
            model_name='tache',
            name='ok',
        ),
        migrations.DeleteModel(
            name='HistoricalTache',
        ),
        migrations.DeleteModel(
            name='HistoricalTechnicienTache',
        ),
    ]