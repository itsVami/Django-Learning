from django import template
from ..models import Category

register = template.Library()

@register.simple_tag
def Web_Title ():
    return "موبایل فروشی اکبر و پسران"

@register.inclusion_tag('blog/partials/category_navbar.html')
def Category_Navbar ():
    return {
        "category" : Category.objects.filter(Status=True)
    }

@register.inclusion_tag('registration/partials/link.html')
def link(request , link_name , content):
    return {
        "request" : request ,
        "link_name" : link_name ,
        "link" : "account:{}".format(link_name) ,
        "content" : content ,
    }
