# Generated by Django 4.2.6 on 2024-02-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='topic/icons'),
        ),
    ]
