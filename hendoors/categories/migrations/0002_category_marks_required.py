# Generated by Django 2.0.4 on 2018-04-30 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='marks_required',
            field=models.IntegerField(default=0),
        ),
    ]
