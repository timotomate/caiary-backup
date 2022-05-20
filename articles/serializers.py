from rest_framework import serializers
from .models import Article
from users.models import User

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['emotion', 'location', 'menu', 'weather', 'song', 'point', 'content',
        'image', 'user', 'created', 'liked', 'num_liked']
        

"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image_url')
"""