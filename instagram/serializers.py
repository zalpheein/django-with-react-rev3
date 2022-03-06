from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post


# 2차 깊이의 JSON 직렬화
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class PostSerializer(serializers.ModelSerializer):
    # 1차 깊이의 JSON 직렬화
    # username = serializers.ReadOnlyField(source='author.username')
    #
    # class Meta:
    #     model = Post
    #     # fields = "__all__"
    #     fields = ['pk', 'username', 'message', 'created_at', 'updated_at']
    """
        {
            "pk": 1,
            "username": "zalphee",
            "message": "첫 번째 포스팅",
            "created_at": "2022-02-24T08:27:09.187318Z",
            "updated_at": "2022-02-24T08:27:09.187318Z"
        },
    """

    # 2차 깊이의 JSON 직렬화
    # author = AuthorSerializer()
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['pk', 'author_username', 'message', 'created_at', 'updated_at', 'is_public']

    """
     {
            "pk": 1,
            "author": {
                "username": "zalphee",
                "email": ""
            },
            "message": "첫 번째 포스팅",
            "created_at": "2022-02-24T08:27:09.187318Z",
            "updated_at": "2022-02-24T08:27:09.187318Z"
        },
    """







