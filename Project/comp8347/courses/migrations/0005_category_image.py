# Generated by Django 4.2.2 on 2023-07-23 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]
