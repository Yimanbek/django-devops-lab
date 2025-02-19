from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6) 

    class Meta:
        model = User
        fields = ["id", "email", "name", "password", "is_active"]
        read_only_fields = ["id", "is_active", "token"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )
        Token.objects.create(user = user)
        return user