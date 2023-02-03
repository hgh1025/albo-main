# Generated by Django 3.2.5 on 2023-02-01 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20230110_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_name',
            field=models.ForeignKey(db_column='user_name', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to='main.user'),
        ),
        migrations.AlterField(
            model_name='item',
            name='user_name',
            field=models.ForeignKey(db_column='user_name', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='main.user'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
