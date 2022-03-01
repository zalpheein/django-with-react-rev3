from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from .models import Post


# CBV 방식으로 구현
# generics.ListAPIView : 리스트 직렬화만 처리
# generics.ListCreateAPIView : 리스트와 생성 직렬화 둘다 처리
class PublicPostListAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(is_public=True)
    serializer_class = PostSerializer


# CBV 방식으로 구현
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # dispatch 함수는 장고 클래스 기반 뷰에서 실제 요청이 될 때마다 호출 되는 함수
    def dispatch(self, request, *args, **kwargs):
        print("request.body :", request.body)       # print() 비추... logger() 추천
        print("request.POST :", request.POST)
        # 예를 들어 등록 할 때, 다음과 같이 2가지 방식으로 저장이 가능...
        # --json + POST : request.body 에 내용이 담겨 서버에 전달
        # --form + POST : request.POST 에 내용이 담저 서버에 전달

        return super().dispatch(request, *args, **kwargs)


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
