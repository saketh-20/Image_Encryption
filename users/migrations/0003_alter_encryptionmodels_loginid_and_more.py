# Generated by Django 4.1.1 on 2023-10-02 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_encryptionmodels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptionmodels',
            name='loginid',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='encryptionmodels',
            name='xorShiftKey',
            field=models.CharField(max_length=100),
        ),
    ]
