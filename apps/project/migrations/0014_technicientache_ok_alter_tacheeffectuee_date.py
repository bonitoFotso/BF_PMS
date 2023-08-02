# Generated by Django 4.2.1 on 2023-08-01 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_tache_ok_delete_historicaletat'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicientache',
            name='ok',
            field=models.BooleanField(default=1, verbose_name='tache effectuer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tacheeffectuee',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name="Date d'effectuation"),
        ),
    ]