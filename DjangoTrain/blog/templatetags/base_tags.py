from django import template
from ..models import Category , Article

from datetime import datetime , timedelta
from django.db.models import Count , Q

register = template.Library()

@register.simple_tag
def Web_Title ():
    return "موبایل فروشی اکبر و پسران"

@register.inclusion_tag('blog/partials/category_navbar.html')
def Category_Navbar ():
    return {
        "category" : Category.objects.filter(Status=True)
    }

@register.inclusion_tag('blog/partials/popular_article.html')
def Popular_Article ():
    last_mounth = datetime.today() - timedelta(days = 30)
    return {
        "popular_article" : Article.objects.published().annotate(count=Count('hits' , filter= Q(articlehit__created__gt = last_mounth))).order_by('-count' , '-Publish')[:5]
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
