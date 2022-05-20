from django.urls import path, include

from rest_framework import routers

from articles.views import ArticleViewSet
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'', ArticleViewSet, basename='Articles')


urlpatterns = [
    path('', include(router.urls)),
    path('post/', views.post_articles, name = 'post_articles'),
    path('get/', views.get_articles, name = 'get_articles'),
    # 특정 상대방의 전체 게시글 가져오기
    # 특정 상대방의 특정 연, 월에 작성된 게시글 가져오기 기능(request로 연, 월 보냄)
    path('get_all/user_<int:pk>/', views.get_all_friends_articles, name = 'get_all_friends_articles'),
    path('get/user_<int:pk>/', views.get_friends_articles, name = 'get_friends_articles'),

    path('get_all/', views.get_allarticles, name = 'get_allarticles'),
    path('get_single_article/<int:pk>/', views.get_single_article, name = 'get_single_article'),
    path('update/<int:pk>/', views.update_articles, name = 'update_articles'),
    path('delete/<int:pk>/', views.delete_articles, name = 'delete_articles'),
    path('<int:pk>/like/', views.post_like_articles, name = 'post_like_articles'),
    path('<int:pk>/unlike/', views.post_unlike_articles, name = 'post_unlike_articles')
]