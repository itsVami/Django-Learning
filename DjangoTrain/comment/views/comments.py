from pickle import FALSE
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages

from comment.models import Comment
from comment.forms import CommentForm
from comment.utils import get_comment_from_key, get_user_for_request, CommentFailReason
from comment.mixins import CanCreateMixin, CanEditMixin, CanDeleteMixin
from comment.responses import UTF8JsonResponse
from comment.messages import EmailError
from comment.views import CommentCreateMixin, BaseCommentView

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class CreateComment(CanCreateMixin, CommentCreateMixin):
    comment = None
    email_service = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.comment
        return context

    def get_template_names(self):
        if self.request.user.is_anonymous or self.comment.is_parent:
            return 'comment/comments/base.html'
        else:
            return 'comment/comments/child_comment.html'

    def form_valid(self, form):
        user = get_user_for_request(self.request)
        comment_content = form.cleaned_data['content']
        email = form.cleaned_data.get('email', None)
        time_posted = timezone.now()
        temp_comment = Comment(
            content_object=self.model_obj,
            content=comment_content,
            user=user,
            parent=self.parent_comment,
            email=email or user.email,
            posted=time_posted
        )
        self.comment = self.perform_create(temp_comment, self.request)
        self.data = render_to_string(self.get_template_names(), self.get_context_data(), request=self.request)
        #Email_Config
        Current_site = get_current_site(self.request)
        Article = self.comment.content_object
        Author_email = Article.Author.email
        User_email = self.comment.user.email
        if Author_email == User_email :
            Author_email = False
            User_email = False

        Parent_Email = False
        if self.comment.parent :
            Parent_Email = self.comment.parent.user.email
            if Parent_Email in [Author_email , User_email]:
                Parent_Email = False
        
        if Author_email:
            Email = EmailMessage(
                        'دیدگاه جدید', 
                        'دیدگاه جدیدی برای مقاله "{}" که شما نویسنده آن هستید ثبت شده. برای مشاهده روی لینک مقابل کلیک کنید.  {}{}'.format(Article , Current_site , reverse('blog:details' , kwargs={'slug':Article.Slug})), 
                        to=[Author_email],
            )
            Email.send()

            if User_email:
                Email = EmailMessage(
                        'دیدگاه شما فرستاده شد.', 
                        'دیدگاه شما نسبت به پست "{}" دریافت شد. باتشکر از شما. '.format(Article), 
                        to=[User_email],
            )
            Email.send()

            if Parent_Email:
                Email = EmailMessage(
                        'به دیدگاه شما پاسخی داده شده.', 
                        ' پاسخ جدیدی برای دیدگاهی که شمادر مقاله"{}"  نوشتید ثبت شده. برای مشاهده روی لینک مقابل کلیک کنید.  {}{}'.format(Article , Current_site , reverse('blog:details' , kwargs={'slug':Article.Slug})), 
                        to=[Parent_Email],
            )
            Email.send()

        return UTF8JsonResponse(self.json())

    def form_invalid(self, form):
        self.error = EmailError.EMAIL_INVALID
        self.status = 400
        return UTF8JsonResponse(self.json(), status=self.status)


class UpdateComment(CanEditMixin, BaseCommentView):
    comment = None

    def get_object(self):
        self.comment = get_object_or_404(
            Comment.objects.select_related('user', 'flag', 'reaction'),
            pk=self.kwargs.get('pk')
        )
        return self.comment

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['comment_form'] = CommentForm(instance=self.comment, request=self.request)
        context['comment'] = self.comment
        self.data = render_to_string('comment/comments/update_comment.html', context, request=self.request)
        return UTF8JsonResponse(self.json())

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, instance=self.comment, request=self.request)
        context = self.get_context_data()
        if form.is_valid():
            form.save()
            context['comment'] = self.comment
            self.data = render_to_string('comment/comments/comment_content.html', context, request=self.request)
            return UTF8JsonResponse(self.json())


class DeleteComment(CanDeleteMixin, BaseCommentView):
    comment = None

    def get_object(self):
        self.comment = get_object_or_404(
            Comment.objects.select_related('user', 'flag', 'reaction'),
            pk=self.kwargs.get('pk')
        )
        return self.comment

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["comment"] = self.comment
        context['has_parent'] = not self.comment.is_parent
        self.data = render_to_string('comment/comments/comment_modal.html', context, request=request)
        return UTF8JsonResponse(self.json())

    def post(self, request, *args, **kwargs):
        self.comment.delete()
        context = self.get_context_data()
        self.data = render_to_string('comment/comments/base.html', context, request=self.request)
        return UTF8JsonResponse(self.json())


class ConfirmComment(CommentCreateMixin):

    @staticmethod
    def _handle_invalid_comment(comment, request):
        if comment.why_invalid == CommentFailReason.BAD:
            messages.error(request, EmailError.BROKEN_VERIFICATION_LINK)
        elif comment.why_invalid == CommentFailReason.EXISTS:
            messages.warning(request, EmailError.USED_VERIFICATION_LINK)

    def get(self, request, *args, **kwargs):
        key = kwargs.get('key', None)
        temp_comment = get_comment_from_key(key)
        self._handle_invalid_comment(temp_comment, request)

        if not temp_comment.is_valid:
            return render(request, template_name='comment/anonymous/discarded.html')

        comment = self.perform_save(temp_comment.obj, request)

        return redirect(comment.get_url(request))
