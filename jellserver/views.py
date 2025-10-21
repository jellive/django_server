from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Post
from .serializers import PostSerializer, PostListSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    게시물 ViewSet

    list: 게시물 목록 조회
    retrieve: 게시물 상세 조회
    create: 게시물 생성
    update: 게시물 수정
    partial_update: 게시물 부분 수정
    destroy: 게시물 삭제
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['div', 'deleted', 'writer']
    search_fields = ['title', 'context', 'writer']
    ordering_fields = ['cdatetime', 'udatetime', 'title']
    ordering = ['-cdatetime']

    def get_serializer_class(self):
        """액션에 따라 다른 시리얼라이저 사용"""
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def get_queryset(self):
        """기본적으로 삭제되지 않은 게시물만 조회"""
        queryset = super().get_queryset()
        include_deleted = self.request.query_params.get('include_deleted', 'false')
        if include_deleted.lower() != 'true':
            queryset = queryset.filter(deleted=False)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(name='div', description='구분', required=True, type=str),
        ],
    )
    @action(detail=False, methods=['get'], url_path='by-div/(?P<div>[^/.]+)')
    def by_div(self, request, div=None):
        """특정 구분의 게시물 조회"""
        posts = self.get_queryset().filter(div=div)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        """게시물 소프트 삭제"""
        post = self.get_object()
        post.deleted = True
        post.save()
        return Response({'status': 'deleted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        """삭제된 게시물 복구"""
        post = self.get_object()
        post.deleted = False
        post.save()
        return Response({'status': 'restored'}, status=status.HTTP_200_OK)
