# Generated by Django 4.2.1 on 2023-06-09 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tache',
            options={'ordering': ['createdAt'], 'verbose_name': 'Tache', 'verbose_name_plural': 'Taches'},
        ),
        migrations.RemoveField(
            model_name='tache',
            name='agence',
        ),
    ]
