# Generated by Django 2.0.4 on 2018-04-20 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
                ('voting_open', models.BooleanField(default=False)),
            ],
        ),
    ]
