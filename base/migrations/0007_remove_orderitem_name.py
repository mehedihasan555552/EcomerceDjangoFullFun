# Generated by Django 3.1 on 2021-05-09 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_orderitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='name',
        ),
    ]
