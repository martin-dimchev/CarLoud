from rest_framework import serializers
from carLoudApp.interactions.models import Comment, ProjectPost

from carLoudApp.accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=ProjectPost.objects.all())
    created_at = serializers.DateTimeField(format='%H:%M', read_only=True)

    class Meta:
        model = Comment
        fields = ['id','user', 'post', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']
