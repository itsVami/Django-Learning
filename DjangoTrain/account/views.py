from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , CreateView , UpdateView , DeleteView
from blog.models import Article
from .mixins import FieldsMixin , FormValidMixin , AuthorAccessMixin , DeleteAccessMixin
from django.urls import reverse_lazy
from .models import User
from .forms import ProfileForm


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


class ArticleDelete(DeleteAccessMixin , DeleteView):
    template_name = "registration/article_confirm_delete.html"
    model = Article
    success_url = reverse_lazy('account:home')


class Profile(UpdateView):
    template_name = "registration/profile.html"
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
