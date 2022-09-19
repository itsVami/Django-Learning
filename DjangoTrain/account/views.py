from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , CreateView , UpdateView
from blog.models import Article
from .mixins import FieldsMixin , FormValidMixin , AuthorAccessMixin


# Create your views here.

class ArticleList(LoginRequiredMixin , ListView):
    template_name = "registration/home.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(Author = self.request.user)
            

class ArticleCreate(LoginRequiredMixin , FieldsMixin , FormValidMixin , CreateView):
    template_name = "registration/article_create_update.html"
    model = Article


class ArticleUpdate(AuthorAccessMixin , FieldsMixin , FormValidMixin , UpdateView):
    template_name = "registration/article_create_update.html"
    model = Article





