# Generated by Django 4.0.5 on 2022-09-18 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_author_user_special_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Is_author',
            field=models.BooleanField(default=False, verbose_name='کاربر ویژه'),
        ),
    ]