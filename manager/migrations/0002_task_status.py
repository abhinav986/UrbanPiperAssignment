# Generated by Django 2.0.2 on 2019-03-01 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]