# Generated by Django 3.0.6 on 2020-05-29 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200528_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writeup',
            name='content',
            field=models.TextField(default='Content here'),
        ),
    ]
