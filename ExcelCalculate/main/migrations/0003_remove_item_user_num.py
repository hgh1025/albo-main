# Generated by Django 4.1.3 on 2022-11-26 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_item_user_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='user_num',
        ),
    ]
