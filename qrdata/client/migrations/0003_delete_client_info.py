# Generated by Django 4.2.4 on 2023-09-19 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_client_data_photo_client_info'),
    ]

    operations = [
        migrations.DeleteModel(
            name='client_info',
        ),
    ]