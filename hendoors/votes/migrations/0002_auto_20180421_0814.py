# Generated by Django 2.0.4 on 2018-04-21 08:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
        ('entries', '0003_auto_20180421_0218'),
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('user', 'category', 'entry')},
        ),
    ]
