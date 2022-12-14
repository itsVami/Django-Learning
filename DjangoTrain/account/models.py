from email.policy import default
from enum import unique
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True , verbose_name='ایمیل' )
    Profile_Avatar = models.ImageField(upload_to="Profile" , default="Profile/default_avatar.png" , verbose_name='عکس پروفایل')
    Is_author = models.BooleanField(default=False , verbose_name='وضعیت نویسندگی')
    Special_user = models.DateTimeField(default=timezone.now , verbose_name ='کاربر ویژه تا')

    def is_special_user(self):
        if self.Special_user > timezone.now() :
            return True
        else:
            return False
    is_special_user.boolean = True
    is_special_user.short_description = "وضعیت کاربر ویژه"