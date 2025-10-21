import pytest
from django.test import TestCase
from jellserver.models import Post


class PostModelTest(TestCase):
    """Post 모델 테스트"""

    def setUp(self):
        """테스트 데이터 설정"""
        self.post = Post.objects.create(
            title='테스트 제목',
            context='테스트 내용',
            div='notice',
            writer='테스터',
        )

    def test_post_creation(self):
        """게시물 생성 테스트"""
        self.assertEqual(self.post.title, '테스트 제목')
        self.assertEqual(self.post.context, '테스트 내용')
        self.assertEqual(self.post.div, 'notice')
        self.assertEqual(self.post.writer, '테스터')
        self.assertFalse(self.post.deleted)

    def test_post_str(self):
        """게시물 문자열 표현 테스트"""
        expected = '[notice] 테스트 제목 - 테스터'
        self.assertEqual(str(self.post), expected)

    def test_post_timestamps(self):
        """타임스탬프 테스트"""
        self.assertIsNotNone(self.post.cdatetime)
        self.assertIsNotNone(self.post.udatetime)

    def test_post_soft_delete(self):
        """소프트 삭제 테스트"""
        self.post.deleted = True
        self.post.save()
        self.assertTrue(self.post.deleted)


@pytest.mark.django_db
class TestPostModelPytest:
    """Pytest를 사용한 Post 모델 테스트"""

    def test_create_post(self):
        """게시물 생성 테스트 (pytest)"""
        post = Post.objects.create(
            title='Pytest 제목',
            context='Pytest 내용',
            div='free',
            writer='pytest_user',
        )
        assert post.title == 'Pytest 제목'
        assert post.deleted is False
        assert post.id is not None
