# Generated by Django 4.2.1 on 2023-06-13 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_remove_tache_technicien_tache_technicien'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicientache',
            name='nom',
            field=models.CharField(default=1, max_length=50, verbose_name='equipe'),
            preserve_default=False,
        ),
    ]