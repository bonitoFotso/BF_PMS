# Generated by Django 4.2.1 on 2023-07-03 06:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0004_alter_technicientache_technicien"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tache",
            name="agence",
        ),
    ]