# Generated by Django 4.0.4 on 2022-10-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincsr', '0019_alter_ngotable_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ngorep',
            name='fname',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='ngorep',
            name='lname',
            field=models.CharField(max_length=256, null=True),
        ),
    ]