# Generated by Django 3.1.7 on 2021-03-15 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210315_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passevents',
            name='event_stamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
