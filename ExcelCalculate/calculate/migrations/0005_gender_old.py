# Generated by Django 3.2.5 on 2023-01-09 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0004_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('남자', '남자'), ('여자', '여자')], max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Old',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(null=True)),
            ],
        ),
    ]
