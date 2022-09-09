# Generated by Django 4.0.5 on 2022-08-29 14:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200, verbose_name='عنوان دسته بندی')),
                ('Slug', models.SlugField(max_length=100, unique=True, verbose_name='آدرس دسته یندی')),
                ('Status', models.BooleanField(verbose_name='نمایش داده شود؟')),
                ('Position', models.ImageField(upload_to='', verbose_name='پوزیشن دسته بندی')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['Position'],
            },
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'مقاله', 'verbose_name_plural': 'مقالات'},
        ),
        migrations.AlterField(
            model_name='article',
            name='Description',
            field=models.TextField(verbose_name='توضیحات مقاله'),
        ),
        migrations.AlterField(
            model_name='article',
            name='Publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار '),
        ),
        migrations.AlterField(
            model_name='article',
            name='Slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله'),
        ),
        migrations.AlterField(
            model_name='article',
            name='Status',
            field=models.CharField(choices=[('d', 'پیش نویس'), ('p', 'منتشر شده')], max_length=1, verbose_name='وضعیت مقاله'),
        ),
        migrations.AlterField(
            model_name='article',
            name='Thumbnail',
            field=models.ImageField(upload_to='Images', verbose_name='تصویر مقاله'),
        ),
        migrations.AlterField(
            model_name='article',
            name='Title',
            field=models.CharField(max_length=200, verbose_name='عنوان مقاله'),
        ),
    ]
