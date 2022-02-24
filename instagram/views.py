from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from .models import Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# 그냥 하려면 아래와 같이 최소 5종의 분기 처리가 필요한데....
# 위와 같이 rest_framework 을 이용한 PostViewSet 에서 간단하게 모든 분기 처리 대신 함
# def post_list(request):
#     # 목록을 위한 GET 과 등록을 위한 POST 분기 처리 필요.... 최소 2 개 분기 처리 필요
#     pass
#
#
# def post_detail(request):
#     # 상세를 위한 GET 과 업데이트를 위한 PUT 과 삭제를 위한 DELETE 처리 필요... 최소 3 개 분기 처리 필요
#     pass
