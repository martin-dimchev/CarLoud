from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView
from rest_framework.reverse import reverse_lazy
from rest_framework.status import HTTP_403_FORBIDDEN
from urllib3 import request

from carLoudApp.interactions.forms import CommentForm
from carLoudApp.interactions.models import Like, Comment
from carLoudApp.projects.models import ProjectImages


class ToggleLikeView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        image_pk = request.POST.get('image_pk')
        image = ProjectImages.objects.get(pk=image_pk)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, image=image)
        if not created:
            like.delete()
        return redirect(f"{request.META.get('HTTP_REFERER')}#image-{image.pk}")


class CommentsListView(LoginRequiredMixin, ListView):
    template_name = 'interactions/comments-list.html'

    def get_queryset(self):
        image_pk = self.kwargs['image_pk']
        image = ProjectImages.objects.get(pk=image_pk)
        comments = Comment.objects.filter(image=image)
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = ProjectImages.objects.get(pk=self.kwargs['image_pk'])
        context['form'] = CommentForm()
        context['real_back_url'] = self.request.POST.get('real_back_url')
        context['current_back_url'] = f"{self.request.META.get('HTTP_REFERER')}#image-{self.kwargs['image_pk']}"
        return context


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            image = ProjectImages.objects.get(pk=self.kwargs['image_pk'])
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect(f"{request.META.get('HTTP_REFERER')}#comment-{comment.pk}")


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'interactions/comment-edit.html'
    pk_url_kwarg = 'comment_pk'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)

        if comment.user != self.request.user:
            raise Http404
        return comment


    def get_success_url(self):
        image_pk = self.kwargs['image_pk']
        return reverse_lazy('comment-section', kwargs={'image_pk': image_pk})

class CommentDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=kwargs['comment_pk'])
            if comment.user == request.user:
                comment.delete()
                return redirect(f"{request.META.get('HTTP_REFERER')}#id_text")
            return HttpResponse(status=HTTP_403_FORBIDDEN)
        except Comment.DoesNotExist:
            raise Http404

