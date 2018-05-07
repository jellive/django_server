# from django.shortcuts import render
from rest_framework import viewsets
from jellserver.serializers import PostSerializer
from jellserver.models import Post

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
