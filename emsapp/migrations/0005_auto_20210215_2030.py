# Generated by Django 3.1.6 on 2021-02-15 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsapp', '0004_auto_20210211_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
