# Generated by Django 4.1.5 on 2023-02-17 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadmodel',
            name='shopid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]