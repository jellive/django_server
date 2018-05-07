from jellserver.models import Post
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'context', 'writer', 'cdatetime', 'udatetime')
