from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .permissions import IsAuthorOrReadonly
from .serializers import PostSerializer


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
    # PostViewSet 을 사용하기 위해서는 무조건 로그인이 되어 있어야 함을 명시적으로 지정하는 방법
    # 아래와 같은 지정이 없을 경우,
    # 아래의 함수들(perform_create,public , set_public) 을 호출 할 수 없음
    # 즉, 인증이 되어 있음을 보장 받을수 있음
    # permission_classes = [IsAuthenticated]

    # 여러 개의 사용자 정의 permission 을 지정 하는 예시
    permission_classes = [IsAuthenticated, IsAuthorOrReadonly]

    # dispatch 함수는 장고 클래스 기반 뷰에서 실제 요청이 될 때마다 호출 되는 함수
    # def dispatch(self, request, *args, **kwargs):
    #     print("request.body :", request.body)       # print() 비추... logger() 추천
    #     print("request.POST :", request.POST)
    #     # 예를 들어 등록 할 때, 다음과 같이 2가지 방식으로 저장이 가능...
    #     # --json + POST : request.body 에 내용이 담겨 서버에 전달
    #     # --form + POST : request.POST 에 내용이 담저 서버에 전달
    #
    #     return super().dispatch(request, *args, **kwargs)

    # 본 클래스(PostViewSet) 를 활용한 목록에서 조회 조건과 정렬을 지정
    filter_backends = [SearchFilter, OrderingFilter]
    # 조회(필터) 방식을 다음과 같이 세분화 할 수 있음
    # ['^message'] : 입력되는 단어로 시작하는 매칭
    # ['=message'] : 입력된 단어와 정확히 매칭
    # ['@message'] : full text search
    # ['$message'] : 정규식 매칭
    # ['message', '~~~', '~~~'] 으로 확장 사용이 가능함
    search_fields = ['message']
    # 아래 정렬 대상을 지정하지 않을 경우, serializer_class 에 지정된 기본 정렬로 수행됨
    ordering_fields = ['id']    # 정렬을 허용할 필드 지정
    ordering = ['id']           # 디폴트 정렬을 지정




    # 신규 생성, 업데이트, 삭제 시에 추가로 지정해야 할 필드가 있다면... perform_XXX 을 이용
    def perform_create(self, serializer):
        author = self.request.user
        ip = self.request.META['REMOTE_ADDR']
        serializer.save(author=author, ip=ip)

    # is_public=True 인 목록을 얻어 오는 public 이름의 함수 생성
    # 브라우저에서 http://127.0.0.1:8000/post/public/ 호출... 즉, is_public=True 인 리스트를 반환
    @action(detail=False, methods=['GET'])
    def public(self, request):
        qs = self.get_queryset().filter(is_public=True)
        # 아래 방법보다 get_serializer 으로 시리얼라이저 클래스를 찾아서 시리얼라이즈를 만들어주는 방식이 적절함
        # serializer = PostSerializer(qs, many=True)
        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)

    # 특정 포스트의 is_public 의 값을 True 로 설정
    # 브라우저에서 http://127.0.0.1:8000/post/2/set_public/ 호출 시, 이건 브라우저에서 호출하는 GET 요청이므로 수행되지 않음
    # 고로 Shell 에서 http PATCH http://127.0.0.1:8000/post/2/set_public/ 라고 수행 해야지 2번 데이터의
    # is_public 값이 True 로 변경 됨
    @action(detail=True, methods=['PATCH'])
    def set_public(self, request, pk):
        # get_objects_or_404 를 사용 할수도 있으나...get_object 를 사용한 예제
        instance = self.get_object()
        instance.is_public = True
        # 특정 필드만 업데이트 수행
        instance.save(update_fields=['is_public'])
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    # 현재 시점에서 허용되는 URL
    # http://127.0.0.1:8000/post.api
    # http://127.0.0.1:8000/post.json
    # http://127.0.0.1:8000/post/?format=json
    # 즉, 반환 되는 내용에 대한 포멧을 URL 로 지정이 가능 하다는 의미


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
