# Generated by Django 4.2.6 on 2024-07-14 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduation_check', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
