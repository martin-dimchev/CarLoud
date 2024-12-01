from rest_framework import serializers
from .models import Comment, ProjectImages
from carLoudApp.accounts.serializers import UserSerializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    image = serializers.PrimaryKeyRelatedField(queryset=ProjectImages.objects.all())
    created_at = serializers.DateTimeField(format="%H:%M")
    class Meta:
        model = Comment
        fields = ['user', 'image', 'text', 'created_at']
        read_only_fields = ['created_at']
