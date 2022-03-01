from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
# 2개의 URL 을 만들어 줌.. 어디에서? router.urls 에서...
router.register('post', views.PostViewSet)


urlpatterns = (
    path('public/', views.PublicPostListAPIView.as_view()),
    path('', include(router.urls)),
)
