# Generated by Django 4.0.4 on 2022-09-28 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincsr', '0014_rename_ngoname_certificates_ngo_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Certificates',
        ),
        migrations.AddField(
            model_name='ngotable',
            name='pdf',
            field=models.FileField(null=True, upload_to='CSR-Project/Media/'),
        ),
    ]
