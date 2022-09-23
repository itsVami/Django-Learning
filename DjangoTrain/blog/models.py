from django.db import models
from django.utils import timezone
from extentions.utils import jalali_conventor
from django.utils.html import format_html
from account.models import User
from django.urls import reverse


#My_Managers
class ArticleManager(models.Manager):
    def published (self):
        return self.filter(Status = 'p')


class CategoryManager(models.Manager):
    def actived (self):
        return self.filter(Status = True)
    


class Category (models.Model):
    Title = models.CharField(max_length=200 , verbose_name ='عنوان دسته بندی')
    Slug = models.SlugField(max_length=100 , unique=True , verbose_name ='آدرس دسته یندی')
    Parent = models.ForeignKey('self' , default = None , null = True , blank = True , on_delete = models.SET_NULL , related_name = 'children' , verbose_name = 'زیر دسته')
    Status = models.BooleanField(verbose_name ='نمایش داده شود؟')
    Position = models.IntegerField(verbose_name='پوزیشن دسته بندی') 
   
    class Meta :
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['Parent__id' ,'Position']
    
    def __str__(self):
        return self.Title  

    objects = CategoryManager()



class Article (models.Model):
    STATUS_CHOISECS = (
        ('d' , "پیش نویس"), #draft
        ('p' , "منتشر شده"), #publish
        ('c' , "در حال بررسی"), #cheking
        ('b' , "برگشت داده شده"), #backed
    )
    Author = models.ForeignKey(User , null = True , on_delete = models.SET_NULL , related_name = 'articles' , verbose_name = 'نویسنده')
    Title = models.CharField(max_length=200 , verbose_name ='عنوان مقاله')
    Slug = models.SlugField(max_length=100 , unique=True , verbose_name ='آدرس مقاله')
    CategoryRE = models.ManyToManyField(Category , related_name="articles" , verbose_name='دسته بندی')
    Description = models.TextField(verbose_name ='توضیحات مقاله')
    Thumbnail = models.ImageField(upload_to="Images" , verbose_name ='تصویر مقاله')
    Publish = models.DateTimeField(default=timezone.now , verbose_name ='زمان انتشار ')
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    Is_special = models.BooleanField(default= False , verbose_name ='مقاله ویژه')
    Status = models.CharField(max_length=1 , choices=STATUS_CHOISECS , verbose_name ='وضعیت مقاله')

    class Meta :
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-Publish']

    def __str__(self):
        return self.Title

    def jpublish(self):
        return jalali_conventor(self.Publish)
    jpublish.short_description = "زمان انتشار"

    def thumbnail_tag(self):
        return format_html("<img width=95 height=80 style='border-radius: 8px;' src='{}'>".format(self.Thumbnail.url))
    thumbnail_tag.short_description = "عکس"

    def Category_to_str(self):
        return " , ".join([CategoryRE.Title for CategoryRE in self.CategoryRE.actived()])
    Category_to_str.short_description = "دسته بندی"

    def get_absolute_url(self):
        return reverse("account:home")

    objects = ArticleManager()
    