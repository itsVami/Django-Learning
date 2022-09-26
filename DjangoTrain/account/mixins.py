from django.http import Http404
from blog.models import Article
from django.shortcuts import get_object_or_404 , redirect

#My Mixins 

class FieldsMixin():

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ["Author" , "Title" , "Slug" , "CategoryRE" , "Description" , "Thumbnail" , "Publish" , "Is_special" , "Status"]
        elif request.user.Is_author:
            self.fields = ["Title" , "Slug" , "CategoryRE" , "Description" , "Thumbnail" , "Is_special" , "Publish"]
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
        if article.Author == request.user and article.Status in ['d' , 'b'] or request.user.is_superuser :
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You Can Not See This Page.")


class DeleteAccessMixin():
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser :
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("You Can Not See This Page.")


class AuthorsAccessMixin():
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.Is_author :
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('account:profile')
        else:
            return redirect('account:login')
