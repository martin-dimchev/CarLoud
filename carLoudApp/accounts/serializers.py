from rest_framework import serializers
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'profile']

