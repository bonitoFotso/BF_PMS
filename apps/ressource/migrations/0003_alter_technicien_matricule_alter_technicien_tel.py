# Generated by Django 4.2.1 on 2023-06-08 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ressource', '0002_technicien_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technicien',
            name='matricule',
            field=models.CharField(max_length=20, unique=True, verbose_name='matricune'),
        ),
        migrations.AlterField(
            model_name='technicien',
            name='tel',
            field=models.CharField(max_length=20, verbose_name='telephone'),
        ),
    ]
