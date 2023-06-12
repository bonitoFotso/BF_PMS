# Generated by Django 4.2.1 on 2023-06-09 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ressource', '0005_alter_technicien_options_alter_technicien_table'),
        ('project', '0005_remove_technicientache_tache_tache_technicien_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tache',
            name='technicien',
        ),
        migrations.AddField(
            model_name='tache',
            name='technicien',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ressource.technicien', verbose_name='Tecnicien'),
            preserve_default=False,
        ),
    ]
