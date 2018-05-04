# Generated by Django 2.0.5 on 2018-05-04 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='code',
            field=models.CharField(blank=True, help_text='The check-in code for the event; not currently used.', max_length=10),
        ),
    ]
