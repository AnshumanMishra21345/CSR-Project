# Generated by Django 4.0.4 on 2022-09-28 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maincsr', '0013_certificates'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificates',
            old_name='ngoname',
            new_name='ngo_name',
        ),
    ]
