# Generated by Django 3.2.6 on 2022-03-08 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0004_alter_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.CharField(max_length=50),
        ),
    ]