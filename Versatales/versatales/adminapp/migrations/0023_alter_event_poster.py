# Generated by Django 5.0.7 on 2024-08-10 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0022_alter_event_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='posters/'),
        ),
    ]
