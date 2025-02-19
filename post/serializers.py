from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'post', 'sentiment', 'added_at')
        read_only_fields = ('id', 'sentiment')

    def create(self, validated_data):
        return super().create(validated_data)