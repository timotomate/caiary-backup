from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.http import Http404
from rest_framework import routers, serializers, viewsets

class Article(models.Model):

    emotion = models.TextField()
    location = models.TextField()
    menu = models.TextField()
    weather = models.TextField()
    song = models.TextField()
    point = models.IntegerField()
    content = models.TextField()

    image = models.ImageField(upload_to="%Y/%m/%d", blank = True, null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(default = now)
    liked = models.BooleanField(default = False)
    num_liked = models.IntegerField(default = 0)

    def __str__(self):
        return self.content

    def get_object(pk):
        try:
            return Article.objects.get(pk = pk)
        except Article.DoesNotExist:
            raise Http404