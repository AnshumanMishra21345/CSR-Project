# Generated by Django 4.0.4 on 2022-09-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maincsr', '0012_alter_ngotable_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngoname', models.CharField(max_length=256)),
                ('pdf', models.FileField(upload_to='CSR-Project/Media/')),
            ],
        ),
    ]
