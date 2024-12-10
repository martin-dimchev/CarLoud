from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from carLoudApp.accounts.views import UserModel
from carLoudApp.interactions.models import Like, Comment, Follower
from carLoudApp.interactions.serializers import CommentSerializer
from carLoudApp.projects.models import ProjectPost



class LikeToggleAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_pk, *args, **kwargs):

        try:
            post = ProjectPost.objects.get(pk=post_pk)
        except ProjectPost.DoesNotExist:
            post = None

        if post:
            post_likes_pks = post.likes.all().values_list('user', flat=True)
            if request.user.pk not in post_likes_pks:
                Like.objects.create(user=request.user, post=post).save()
                return Response(status=status.HTTP_201_CREATED, data={
                    "liked": True,
                    "likes_count": post.likes.count()
                })
            else:
                Like.objects.filter(user=request.user, post=post).delete()
                Like.objects.filter(user=request.user, post=post).delete()
                return Response(status=status.HTTP_200_OK, data={
                    "liked": False,
                    "likes_count": post.likes.count()
                })
        return Response(status=status.HTTP_404_NOT_FOUND, data={})


class FollowToggleAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        follower = request.user
        is_following_pk = kwargs.get('account_pk')

        try:
            is_following = UserModel.objects.get(pk=is_following_pk)
        except UserModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "error": "No such user"
            })

        if Follower.objects.filter(follower=follower, is_following=is_following).exists():
            Follower.objects.filter(follower=follower, is_following=is_following).delete()
            return Response(status=status.HTTP_200_OK, data={
                "is_followed": False,
            })
        else:
            if is_following != request.user:
                Follower.objects.create(follower=follower, is_following=is_following).save()
                return Response(status=status.HTTP_201_CREATED, data={
                    "is_followed": True,
                })
            return Response(status=status.HTTP_403_FORBIDDEN, data={
                "error": "You cannot follow yourself!"
            })


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentEditView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

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
        user_permissions = request.user.get_all_permissions()
        if comment.user != request.user and 'interactions.delete_comment' not in user_permissions:
            return Response(
                {'success': False, 'error': 'Forbidden: You are not the owner of this comment.'},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(
            {'success': True, 'message': 'Comment deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )