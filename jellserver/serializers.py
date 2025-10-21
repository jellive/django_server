from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """게시물 시리얼라이저"""

    class Meta:
        model = Post
        fields = ['id', 'title', 'context', 'writer', 'div', 'deleted', 'cdatetime', 'udatetime']
        read_only_fields = ['id', 'cdatetime', 'udatetime']

    def validate_title(self, value):
        """제목 검증"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("제목은 최소 2자 이상이어야 합니다.")
        return value.strip()

    def validate_context(self, value):
        """내용 검증"""
        if len(value.strip()) < 1:
            raise serializers.ValidationError("내용을 입력해주세요.")
        return value.strip()


class PostListSerializer(serializers.ModelSerializer):
    """게시물 목록용 간소화된 시리얼라이저"""

    class Meta:
        model = Post
        fields = ['id', 'title', 'writer', 'div', 'deleted', 'cdatetime']
        read_only_fields = fields
