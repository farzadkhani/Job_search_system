from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer for adding custom claims

    params:
        username: username of user
        email: email of user
        usage_type: type of user
    """

    # def validate(self, attrs):
    #     data = super().validate(attrs)

    #     # Add custom data
    #     data["username"] = self.user.username
    #     data["email"] = self.user.email
    #     data["usage_type"] = self.user.usage_type

    #     return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["usage_type"] = user.usage_type

        return token


class BaseRegisterSerializer(serializers.ModelSerializer):
    """
    register serializer for user base on required fields

    fields:
        email: email of user
        password: password of user
        password2: validate password
        usage_type: type of user
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "usage_type",
        )
        extra_kwargs = {
            "usage_type": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs


class JobSeekerRegisterSerializer(BaseRegisterSerializer):
    """
    register serializer for jobseeker
    """

    def create(self, validated_data):
        validated_data.pop("password2", None)
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            usage_type="JobSeeker",
        )
        return user


class EmployerRegisterSerializer(BaseRegisterSerializer):
    """
    register serializer for Employer
    """

    def create(self, validated_data):
        validated_data.pop("password2", None)
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            usage_type="Employer",
        )
        return user



class StaffRegisterSerializer(BaseRegisterSerializer):
    """
    register serializer for Employer
    """

    def create(self, validated_data):
        validated_data.pop("password2", None)
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            usage_type="JobSeeker",
        )
        return user