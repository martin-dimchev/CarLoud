from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from rest_framework.reverse import reverse_lazy
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from carLoudApp.accounts.views import UserModel
from carLoudApp.interactions.forms import CommentForm
from carLoudApp.interactions.models import Like, Comment, Follower
from carLoudApp.interactions.serializers import CommentSerializer
from carLoudApp.projects.models import ProjectPosts



class LikeToggleAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, image_pk, *args, **kwargs):

        try:
            image = ProjectPosts.objects.get(pk=image_pk)
        except ProjectPosts.DoesNotExist:
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

class FollowToggleAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        follower = request.user
        is_following_pk = kwargs.get('account_pk')

        try:
            is_following = UserModel.objects.get(pk=is_following_pk)
        except UserModel.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND, data={
                "error": "No such user"
            })

        if Follower.objects.filter(follower=follower, is_following=is_following).exists():
            Follower.objects.filter(follower=follower, is_following=is_following).delete()
            return Response(status=HTTP_200_OK, data={
                "is_followed": False,
            })
        else:
            if is_following != request.user:
                Follower.objects.create(follower=follower, is_following=is_following).save()
                return Response(status=HTTP_201_CREATED, data={
                    "is_followed": True,
                })
            return Response(status=HTTP_403_FORBIDDEN, data={
                "error": "You cannot follow yourself!"
            })








class CommentsListView(LoginRequiredMixin, ListView):
    template_name = 'interactions/comments-list.html'

    def get_queryset(self):
        image_pk = self.kwargs['image_pk']
        image = ProjectPosts.objects.get(pk=image_pk)
        comments = Comment.objects.filter(image=image)
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = ProjectPosts.objects.get(pk=self.kwargs['image_pk'])
        context['form'] = CommentForm()
        context['real_back_url'] = self.request.POST.get('real_back_url')
        context['current_back_url'] = f"{self.request.META.get('HTTP_REFERER')}#image-{self.kwargs['image_pk']}"
        return context


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentEditView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({"error": "You do not have permission to edit this comment."},
                            status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(comment, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment updated successfully!", "text": serializer.data['text']},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.user != request.user:
            return Response(
                {'success': False, 'error': 'Forbidden: You are not the owner of this comment.'},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(
            {'success': True, 'message': 'Comment deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )