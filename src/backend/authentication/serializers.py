from rest_framework import serializers

from .models import User, Profile


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, user_data):
        return User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField()

    class Meta:
        model = Profile
        fields = ("about_me", "profile_picture", "banner_image")


class UserSerializer(UserCreateSerializer):
    password = None
    email = None
    profile = UserProfileSerializer()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            "id",
            "username",
            "is_staff",
            "profile",
            "is_online",
            "last_online",
            "date_joined",
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
