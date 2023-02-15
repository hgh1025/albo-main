# Generated by Django 3.2.5 on 2023-02-05 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_img', models.ImageField(blank=True, null=True, upload_to='trade_images/')),
                ('item_price', models.IntegerField(null=True)),
                ('item_date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_date', models.DateTimeField(auto_now_add=True)),
                ('user_email', models.EmailField(max_length=254, unique=True)),
                ('user_password', models.CharField(max_length=100)),
                ('user_validate', models.BooleanField(default=False)),
                ('gender', models.CharField(choices=[('남자', '남자'), ('여자', '여자')], max_length=5, null=True)),
                ('age', models.IntegerField(null=True)),
                ('year', models.IntegerField(null=True)),
                ('month', models.IntegerField(null=True)),
                ('day', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'user_tb',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=20)),
                ('trade_status', models.CharField(choices=[('거래 전', '거래 전'), ('거래 완료', '거래 완료')], default='거래 전', max_length=5, null=True)),
                ('item_price', models.IntegerField(null=True)),
                ('item_content', models.TextField(max_length=200)),
                ('item_img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user_name', models.ForeignKey(db_column='user_name', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='main.user')),
            ],
            options={
                'db_table': 'item_tb',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('item_id', models.ForeignKey(db_column='item_id', on_delete=django.db.models.deletion.CASCADE, related_name='post', to='main.item')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='main.comment')),
                ('user_name', models.ForeignKey(db_column='user_name', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to='main.user')),
            ],
            options={
                'ordering': ['-comment_date'],
            },
        ),
    ]
