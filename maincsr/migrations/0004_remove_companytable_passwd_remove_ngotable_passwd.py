# Generated by Django 4.0.4 on 2022-05-27 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maincsr', '0003_alter_companytable_total_amount_donated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companytable',
            name='passwd',
        ),
        migrations.RemoveField(
            model_name='ngotable',
            name='passwd',
        ),
    ]