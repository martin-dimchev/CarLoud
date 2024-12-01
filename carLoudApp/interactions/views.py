from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.reverse import reverse_lazy
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView


from carLoudApp.interactions.forms import CommentForm
from carLoudApp.interactions.models import Like, Comment
from carLoudApp.interactions.serializers import CommentSerializer
from carLoudApp.projects.models import ProjectImages



class ToggleLikeAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, image_pk, *args, **kwargs):

        try:
            image = ProjectImages.objects.get(pk=image_pk)
        except ProjectImages.DoesNotExist:
            image = None

        if image:
            image_likes_pks = image.likes.all().values_list('user', flat=True)
            if request.user.pk not in image_likes_pks:
                Like.objects.create(user=request.user, image=image).save()
                return Response(status=HTTP_201_CREATED, data={
                    "liked": True,
                    "likes_count": image.likes.count()
                })
            else:
                Like.objects.filter(user=request.user, image=image).delete()
                return Response(status=HTTP_200_OK, data={
                    "liked": False,
                    "likes_count": image.likes.count()
                })
        return Response(status=HTTP_404_NOT_FOUND, data={})


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


class CommentCreateView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, image_pk, *args, **kwargs):
        user = request.user
        print(user)
        try:
            image = ProjectImages.objects.get(pk=image_pk)
        except ProjectImages.DoesNotExist:
            image = None

        if image:
            comment = Comment.objects.create(
            user=user,
            image=image,
            text=request.data.get('text')
        )
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=HTTP_403_FORBIDDEN, data={})




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
