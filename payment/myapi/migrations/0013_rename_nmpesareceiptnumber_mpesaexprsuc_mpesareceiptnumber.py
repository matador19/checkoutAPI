# Generated by Django 3.2.6 on 2022-03-09 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0012_auto_20220309_1656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mpesaexprsuc',
            old_name='NMpesaReceiptNumber',
            new_name='MpesaReceiptNumber',
        ),
    ]