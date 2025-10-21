"""Factory definitions for test data generation using Factory Boy"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from jellserver.models import Post

fake = Faker(['ko_KR', 'en_US'])


class PostFactory(DjangoModelFactory):
    """Post 모델 팩토리"""

    class Meta:
        model = Post

    title = factory.Faker('sentence', nb_words=5, locale='ko_KR')
    context = factory.Faker('paragraph', nb_sentences=5, locale='ko_KR')
    div = factory.Iterator(['notice', 'free', 'qna', 'announcement'])
    writer = factory.Faker('name', locale='ko_KR')
    deleted = False

    @factory.post_generation
    def set_deleted(obj, create, extracted, **kwargs):
        """일부 게시물을 삭제 상태로 설정"""
        if extracted:
            obj.deleted = extracted


class DeletedPostFactory(PostFactory):
    """삭제된 게시물 팩토리"""

    deleted = True


class NoticePostFactory(PostFactory):
    """공지사항 팩토리"""

    div = 'notice'
    title = factory.Sequence(lambda n: f'[공지] {fake.sentence(nb_words=4)}')


class QnaPostFactory(PostFactory):
    """Q&A 팩토리"""

    div = 'qna'
    title = factory.Sequence(lambda n: f'[질문] {fake.sentence(nb_words=4)}')
    context = factory.LazyFunction(lambda: f"{fake.paragraph()}\\n\\n문의사항입니다.")
