# Generated by Django 3.1.2 on 2021-04-29 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='icon',
            field=models.ImageField(default='users/default.png', upload_to='users/', verbose_name='ユーザーアイコン'),
        ),
    ]
