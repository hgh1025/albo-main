# Generated by Django 3.2.5 on 2022-12-15 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_item_item_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='trade_date',
            new_name='item_date',
        ),
    ]
