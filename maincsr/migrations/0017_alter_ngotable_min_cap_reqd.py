# Generated by Django 4.0.4 on 2022-10-02 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincsr', '0016_alter_ngotable_no_of_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ngotable',
            name='min_cap_reqd',
            field=models.BigIntegerField(null=True),
        ),
    ]