# Generated by Django 3.2.6 on 2022-03-09 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0013_rename_nmpesareceiptnumber_mpesaexprsuc_mpesareceiptnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesaexprsuc',
            name='PhoneNumber',
            field=models.IntegerField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='mpesaexprsuc',
            name='TransactionDate',
            field=models.IntegerField(max_length=40, null=True),
        ),
    ]
