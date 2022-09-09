from pickle import FALSE
from django.contrib import admin
from .models import Article , Category

#َAdmin Page Header
admin.site.site_header = "ادمین پنل وبسایت"


#Actions
def make_published(modeladmin , request , queryset):
    queryset = queryset.update(Status='p')
    if queryset == 1 :
        message_bit = "منتشر شد"
    else :
        message_bit = "منتشر شدند"
    modeladmin.message_user(request , "{} مقاله {}.".format(queryset , message_bit))
make_published.short_description = "منتشر کردن مقالات انتخاب شده"

def make_draft(modeladmin , request, queryset):
    queryset = queryset.update(Status='d')
    if queryset == 1 :
        message_bit = "پیش نویس شد"
    else :
        message_bit = "پیش نویس شدند"
    modeladmin.message_user(request , "{} مقاله {}.".format(queryset , message_bit))
make_draft.short_description = "پیش نویس کردن مقالات انتخاب شده"

def show(modeladmin , request , queryset):
    queryset = queryset.update(Status=True)
    if queryset == 1 :
        message_bit = "فعال شد"
    else :
        message_bit = "فعال شدند"
    modeladmin.message_user(request , "{} دسته بندی {}.".format(queryset , message_bit))
show.short_description = "فعال کردن دسته بندی های انتخاب شده"

def dontshow(modeladmin , request, queryset):
    queryset = queryset.update(Status=False)
    if queryset == 1 :
        message_bit = "غیر فعال شد"
    else :
        message_bit = "غیر فعال شدند"
    modeladmin.message_user(request , "{} دسته بندی  {}.".format(queryset , message_bit))
dontshow.short_description = "غیر فعال کردن دسته بندی های انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Position' ,'Title' , 'Parent' , 'Slug' , 'Status') 
    list_filter = (['Status'])
    search_fields = ('Title' , 'Slug')
    prepopulated_fields = {'Slug' : ('Title' ,)}   #Auto_Slug
    actions = [show , dontshow ]

admin.site.register(Category , CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('Title' , 'thumbnail_tag' , 'Slug' , 'jpublish' , 'Status' , 'Category_to_str')
    list_filter = ('Publish' , 'Status')
    search_fields = ('Title' , 'Description')
    prepopulated_fields = {'Slug' : ('Title' ,)}   #Auto_Slug
    ordering = ['-Status' , '-Publish']
    actions = [make_published , make_draft ]

    def Category_to_str(self , obj):
        return " , ".join([Category.Title for Category in obj.category_publish()])
    Category_to_str.short_description = "دسته بندی"

admin.site.register(Article , ArticleAdmin)


