# Generated by Django 3.2.19 on 2023-07-30 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uzers', '0002_auto_20230730_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='time',
            field=models.TimeField(default=None),
        ),
    ]
