import json
from django.http import JsonResponse
from requests import Response
from rest_framework import viewsets, status, routers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

from .models import Article
from .serializers import ArticleSerializer
from articles import serializers
class ArticleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer

    queryset = Article.objects.all()

    def list(self, request):
        articles = Article.objects.filter(user=request.user)

        response = {
            'data': list(articles.values())
        }

        return JsonResponse(response)


# 01. C - 게시글 작성
@api_view(['POST'])
@permission_classes([])
def post_articles(request):
    
    user = request.user
    body = json.loads(request.POST["data"])
    image = request.FILES["image"]

    article = Article(
        emotion = body['emotion'],
        location = body['location'],
        menu = body['menu'],
        weather = body['weather'],
        image = image,
        song = body['song'],
        point = body['point'],
        content = body['content'],
        user = user)
    article.save()

    serializers = ArticleSerializer(article)

    return JsonResponse(serializers.data)

    # if serializer.is_valid():
    #     serializer.save()
    #     return JsonResponse(serializer.data)
    # else:
    #     return JsonResponse(serializer.error_messages())


# 02. R - 상대방 게시글 전체 목록
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_friends_articles(request, pk):
    article = Article.objects.filter(user = pk)

    response = {
        'success' : True,
        'data' : list(article.values())
    }
    
    return JsonResponse(response)


# 02. R - 상대방 게시글 검색해셔 가져오기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends_articles(request, pk):
    year = int(request.data["year"])
    month = int(request.data["month"])

    article = Article.objects.filter(user = pk, created__year = year, created__month = month)

    response = {
        'success' : True,
        'data' : list(article.values())
    }
    
    return JsonResponse(response)


# 02. R - 내 게시글 목록(get)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_articles(request):
    year = int(request.data["year"])
    month = int(request.data["month"])
    
    articles = Article.objects.filter(user = request.user, created__year = year, created__month = month)
    
    response = {
        'success' : True,
        'data': list(articles.values()),
    }

    return JsonResponse(response)


# 02. R - 피드 일기 목록(get_all)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_allarticles(request):
    article = Article.objects.all()

    response = {
        'success' : True,
        'data' : list(article.values())
    }
    
    return JsonResponse(response)


# 02. R - 게시글 한 개만 가져오기(get_single_article/<int:pk>)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_article(request, pk):
    article = Article.get_object(pk)
    
    response = {
        'success' : True,
        'data' : list(article.content)
    }

    return JsonResponse(response)


# 03. U - 게시글 수정(update/<int:pk>/)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_articles(request, pk):
    article = Article.get_object(pk)
    data = request.data["content"]
    article.content = data
    article.save()

    response = {
        'success' : True,
        'data' : article.content,
    }

    return JsonResponse(response)
    

# 04. D - 게시글 삭제(delete/<int:pk>/)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_articles(request, pk):
    article = Article.get_object(pk)
    article.delete()
    serializer = ArticleSerializer(article)
    return JsonResponse({'success' : True, 'data' : serializer.data })


# 05. 게시글 하트(post/<int:pk>/like/) 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def post_like_articles(request, pk):
    article = Article.get_object(pk)
    article.liked = True
    article.num_liked += 1
    article.save()
    serializer = ArticleSerializer(article)
    return JsonResponse({'success' : True, 'data' : serializer.data })


# 06. 게시글 하트 취소(post/<int:pk>/unlike/)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def post_unlike_articles(request, pk):
    article = Article.get_object(pk)
    if article.num_liked > 0:
        article.liked = False
        article.num_liked -= 1
        article.save()
        serializer = ArticleSerializer(article)
        return JsonResponse({'success' : True, 'data' : serializer.data })
    else:
        return JsonResponse({'success' : False})