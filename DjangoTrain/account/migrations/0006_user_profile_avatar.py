# Generated by Django 4.0.5 on 2022-10-02 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Profile_Avatar',
            field=models.ImageField(blank=True, upload_to='Profile', verbose_name='عکس پروفایل'),
        ),
    ]
