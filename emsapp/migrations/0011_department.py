# Generated by Django 3.1.6 on 2021-03-11 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsapp', '0010_auto_20210304_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
    ]
