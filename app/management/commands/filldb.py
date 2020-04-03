from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Profile, Tag, Like, LikeToAnswer, Answer
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--likes', type=int)
        parser.add_argument('--likes_to_ans', type=int)

    def fill_authors(self, cnt):
        for i in range(cnt):
            u = User(username=f.name())
            u.save()
            Profile.objects.create(
                user=u
            )

    def fill_questions(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Question.objects.create(
                author=Profile.objects.get(id=choice(author_ids)),
                title=f.sentence()[:40],
                text=f.text(),
            )

    def fill_answers(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Answer.objects.create(
                author=Profile.objects.get(id=choice(author_ids)),
                text=f.text(),
                question=Question.objects.get(id=choice(question_ids)),
                )

    def fill_tags(self, cnt):
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            tag = Tag.objects.create(tag_name=f.word())
            for j in range(len(question_ids) // 3):
                Question.objects.get(id=choice(question_ids)).tags.add(tag)

    def fill_likes(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            like = Like.objects.create(
                user=Profile.objects.get(id=choice(author_ids)),
                question=Question.objects.get(id=choice(question_ids)),
                )

    def fill_likes_to_ans(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        answer_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            like = LikeToAnswer.objects.create(
                user=Profile.objects.get(id=choice(author_ids)),
                answer=Answer.objects.get(id=choice(answer_ids)),
                )

    def handle(self, *args, **options):
        if options['authors']:
            self.fill_authors(options.get('authors', 0))
        if options['questions']:
            self.fill_questions(options.get('questions', 0))
        if options['tags']:
            self.fill_tags(options.get('tags', 0))
        if options['answers']:
            self.fill_answers(options.get('answers', 0))
        if options['likes']:
            self.fill_likes(options.get('likes', 0))
        if options['likes_to_ans']:
            self.fill_likes_to_ans(options.get('likes_to_ans', 0))