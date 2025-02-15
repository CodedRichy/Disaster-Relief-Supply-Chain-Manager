# Generated by Django 5.1.6 on 2025-02-15 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DRSCM', '0002_disaster_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='logistics',
            name='end_lat',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logistics',
            name='end_lng',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logistics',
            name='start_lat',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logistics',
            name='start_lng',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
