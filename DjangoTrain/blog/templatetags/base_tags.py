from django import template
from ..models import Category , Article

from datetime import datetime , timedelta
from django.db.models import Count , Q

from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def Web_Title ():
    return "موبایل فروشی اکبر و پسران"

@register.inclusion_tag('blog/partials/category_navbar.html')
def Category_Navbar ():
    return {
        "category" : Category.objects.filter(Status=True)
    }

@register.inclusion_tag('blog/partials/sidebar_article.html')
def Popular_Article ():
    last_mounth = datetime.today() - timedelta(days = 30)
    return {
        "sidebar_article" : Article.objects.published().annotate(count=Count('hits' , filter= Q(articlehit__created__gt = last_mounth))).order_by('-count' , '-Publish')[:5] ,
        "Title" : 'مقالات پر بازدید' ,
    }

@register.inclusion_tag('blog/partials/sidebar_article.html')
def Hot_Article ():
    last_mounth = datetime.today() - timedelta(days = 30)
    content_type_ip = ContentType.objects.get(app_label='blog', model='article').id
    return {
        "sidebar_article" : Article.objects.published().annotate(count=Count('comments' , filter= Q(comments__posted__gt = last_mounth) and Q(comments__content_type_id = content_type_ip))).order_by('-count' , '-Publish')[:5] ,
        "Title" : 'مقالات داغ' ,
    }

@register.inclusion_tag('registration/partials/link.html')
def link(request , link_name , content , classes):
    return {
        "request" : request ,
        "link_name" : link_name ,
        "link" : "account:{}".format(link_name) ,
        "content" : content ,
        "classes" : classes ,
    }
