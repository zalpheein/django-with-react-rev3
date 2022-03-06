from rest_framework import permissions


# 사용자 정의 permission 작성 예시
# 인증이 되어 있지 않으면 Read Only 를 적용
class IsAuthorOrReadonly(permissions.BasePermission):
    # 인증이 된 사용자는 누구나 목록 조회 및 포스팅 등록을 허용 한다는 의미
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # 등록된 포스팅의 경우, 일반 사용자는 조회만 가능하고 그 이외의 수정과 같은 작업들은 오직 작성자만 가능함을 지정
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user