# Generated by Django 4.2.2 on 2023-07-23 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0002_order'),
        ('courses', '0006_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='club',
            field=models.ManyToManyField(to='club.club'),
        ),
    ]
