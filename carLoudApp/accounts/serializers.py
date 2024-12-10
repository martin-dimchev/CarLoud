from rest_framework import serializers

from carLoudApp.accounts.models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'profile']
        read_only_fields = ['id', 'username', 'email', 'full_name', 'profile']

