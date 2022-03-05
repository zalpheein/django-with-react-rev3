from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer
from .models import Post


# ----------------------------------------------------------------
# 리스트 - 시리얼라이즈를 활용한... http://127.0.0.1:8000/public/
# ----------------------------------------------------------------

# generics 을 이용하여 CBV 방식으로 구현
# generics.ListAPIView : 리스트 직렬화만 처리
# generics.ListCreateAPIView : 리스트와 생성 직렬화 둘다 처리
# class PublicPostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.filter(is_public=True)
#     serializer_class = PostSerializer


# APIView 를 이용하여 FBV 방식으로 구현
# class PublicPostListAPIView(APIView):
#
#     def get(self, request):
#         queryset = Post.objects.filter(is_public=True)
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# public_post_list = PublicPostListAPIView.as_view()

# 순수한 함수 기반뷰로 구현
# 반드시, @api_view 라는 장식자가 필요
@api_view(['GET'])
def public_post_list(request):
    queryset = Post.objects.filter(is_public=True)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)

# ----------------------------------------------------------------
# 리스트 - ViewSet 을 활용한.... http://127.0.0.1:8000/post/
# ----------------------------------------------------------------


# CBV 방식으로 구현
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # dispatch 함수는 장고 클래스 기반 뷰에서 실제 요청이 될 때마다 호출 되는 함수
    # def dispatch(self, request, *args, **kwargs):
    #     print("request.body :", request.body)       # print() 비추... logger() 추천
    #     print("request.POST :", request.POST)
    #     # 예를 들어 등록 할 때, 다음과 같이 2가지 방식으로 저장이 가능...
    #     # --json + POST : request.body 에 내용이 담겨 서버에 전달
    #     # --form + POST : request.POST 에 내용이 담저 서버에 전달
    #
    #     return super().dispatch(request, *args, **kwargs)

    # is_public=True 인 목록을 얻어 오는 public 이름의 함수 생성
    @action(detail=False, method=['GET'])
    def public(self, request):
        qs = self.get_queryset().filter(is_public=True)
        # 아래 방법보다 시리얼라이저 클래스를 찾아서 시리얼라이즈를 만들어주는 방식이 적절함
        # serializer = PostSerializer(qs, many=True)
        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)


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
