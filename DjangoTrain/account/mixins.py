from django.http import Http404
from blog.models import Article
from django.shortcuts import get_object_or_404

#My Mixins 

class FieldsMixin():

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ["Author" , "Title" , "Slug" , "CategoryRE" , "Description" , "Thumbnail" , "Publish" , "Status"]
        elif request.user.Is_author:
            self.fields = ["Title" , "Slug" , "CategoryRE" , "Description" , "Thumbnail" , "Publish"]
        else:
            raise Http404("You Can Not See This Page.")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self , form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit = False)
            self.obj.Author = self.request.user
            self.obj.Status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article , pk=pk)
        if article.Author == request.user and article.Status == 'd' or request.user.is_superuser :
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You Can Not See This Page.")


class DeleteAccessMixin():
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser :
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You Can Not See This Page.")