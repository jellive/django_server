"""
Integration Tests

These tests verify that different parts of the system work together correctly.
They test interactions between models, serializers, views, and the database.
"""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from jellserver.models import Post
from jellserver.tests.factories import PostFactory, NoticePostFactory, DeletedPostFactory


@pytest.mark.django_db
class TestPostModelIntegration:
    """Post 모델 통합 테스트"""

    def test_post_creation_with_all_fields(self):
        """모든 필드가 포함된 게시물 생성"""
        post = PostFactory()

        assert post.id is not None
        assert post.title
        assert post.context
        assert post.div in ['notice', 'free', 'qna', 'announcement']
        assert post.writer
        assert post.cdatetime is not None
        assert post.udatetime is not None
        assert not post.deleted

    def test_post_ordering(self):
        """게시물 정렬 테스트"""
        post1 = PostFactory()
        post2 = PostFactory()
        post3 = PostFactory()

        posts = Post.objects.all()
        # 최신순 정렬 확인
        assert posts[0].id == post3.id
        assert posts[1].id == post2.id
        assert posts[2].id == post1.id

    def test_post_filtering_by_div(self):
        """구분별 필터링 통합 테스트"""
        NoticePostFactory.create_batch(3)
        PostFactory.create_batch(2, div='free')

        notice_posts = Post.objects.filter(div='notice')
        free_posts = Post.objects.filter(div='free')

        assert notice_posts.count() == 3
        assert free_posts.count() == 2

    def test_soft_delete_workflow(self):
        """소프트 삭제 워크플로우 테스트"""
        post = PostFactory()
        post_id = post.id

        # 소프트 삭제
        post.deleted = True
        post.save()

        # 데이터베이스에 여전히 존재
        assert Post.objects.filter(id=post_id).exists()

        # deleted 필터로 제외
        active_posts = Post.objects.filter(deleted=False)
        assert post not in active_posts


@pytest.mark.django_db
class TestPostAPIIntegration:
    """Post API 통합 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_create_retrieve_update_delete_workflow(self):
        """CRUD 전체 워크플로우 통합 테스트"""
        # Create
        create_data = {
            'title': '통합 테스트 제목',
            'context': '통합 테스트 내용',
            'div': 'notice',
            'writer': 'Integration Tester',
        }
        create_response = self.client.post(reverse('post-list'), create_data)
        assert create_response.status_code == 201
        post_id = create_response.data['id']

        # Retrieve
        retrieve_response = self.client.get(reverse('post-detail', args=[post_id]))
        assert retrieve_response.status_code == 200
        assert retrieve_response.data['title'] == '통합 테스트 제목'

        # Update
        update_data = {
            'title': '수정된 제목',
            'context': '통합 테스트 내용',
            'div': 'notice',
            'writer': 'Integration Tester',
        }
        update_response = self.client.put(reverse('post-detail', args=[post_id]), update_data)
        assert update_response.status_code == 200
        assert update_response.data['title'] == '수정된 제목'

        # Delete (soft)
        delete_response = self.client.post(reverse('post-soft-delete', args=[post_id]))
        assert delete_response.status_code == 200

        # Verify soft delete
        post = Post.objects.get(id=post_id)
        assert post.deleted is True

    def test_filter_search_pagination_integration(self):
        """필터링, 검색, 페이지네이션 통합 테스트"""
        # 다양한 게시물 생성
        NoticePostFactory.create_batch(15)
        PostFactory.create_batch(10, div='free', title='자유게시판 글')

        # 필터링
        response = self.client.get(reverse('post-list'), {'div': 'notice'})
        assert response.status_code == 200
        assert len(response.data['results']) == 10  # First page
        assert response.data['count'] == 15

        # 검색
        response = self.client.get(reverse('post-list'), {'search': '자유게시판'})
        assert response.status_code == 200
        assert len(response.data['results']) == 10  # First page of search results

        # 페이지네이션
        response = self.client.get(reverse('post-list'), {'page': 2})
        assert response.status_code == 200
        assert 'results' in response.data

    def test_factory_integration(self):
        """Factory와 API 통합 테스트"""
        # Factory로 데이터 생성
        posts = PostFactory.create_batch(5)
        deleted_post = DeletedPostFactory()

        # API로 조회
        response = self.client.get(reverse('post-list'))
        assert response.status_code == 200

        # 삭제되지 않은 게시물만 조회되는지 확인
        post_ids = [p['id'] for p in response.data['results']]
        assert deleted_post.id not in post_ids
        assert len([p for p in posts if p.id in post_ids]) == 5


@pytest.mark.django_db
class TestBusinessLogicIntegration:
    """비즈니스 로직 통합 테스트"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_post_lifecycle(self):
        """게시물 생명주기 통합 테스트"""
        # 1. 게시물 생성
        post = PostFactory(div='notice', deleted=False)

        # 2. 활성 게시물 목록에 포함되는지 확인
        active_posts = Post.objects.filter(deleted=False)
        assert post in active_posts

        # 3. 게시물 수정
        post.title = '수정된 제목'
        post.save()
        post.refresh_from_db()
        assert post.title == '수정된 제목'

        # 4. 소프트 삭제
        post.deleted = True
        post.save()

        # 5. 활성 게시물에서 제외되는지 확인
        active_posts = Post.objects.filter(deleted=False)
        assert post not in active_posts

        # 6. 전체 게시물에는 여전히 포함되는지 확인
        all_posts = Post.objects.all()
        assert post in all_posts

    def test_bulk_operations(self):
        """대량 작업 통합 테스트"""
        # 대량 생성
        posts = PostFactory.create_batch(100)

        # 대량 조회
        assert Post.objects.count() == 100

        # 대량 업데이트
        Post.objects.filter(div='notice').update(deleted=True)
        notice_count = Post.objects.filter(div='notice', deleted=True).count()
        assert notice_count > 0

        # 대량 삭제는 소프트 삭제만 수행
        active_count = Post.objects.filter(deleted=False).count()
        assert active_count < 100
