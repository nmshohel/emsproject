# Generated by Django 3.1.6 on 2021-03-03 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emsapp', '0007_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='emsapp.department'),
            preserve_default=False,
        ),
    ]
