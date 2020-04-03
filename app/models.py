from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
# Create your models here.

def question_counter(question):
    question.likes = len(Like.objects.filter(question = question))
    question.answers = len(Answer.objects.filter(question = question))
    return question


def answer_counter(answer):
    answer.likes = len(LikeToAnswer.objects.filter(answer=answer))
    return answer


def tag_counter(tag):
    tag.usage = len(Question.objects.filter(tags = tag))
    return tag


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, db_index = True)
    avatar = models.ImageField(upload_to = 'uploads/%Y/%m/%d/', default = 'uploads/default/default.png')


class TagManager(models.Manager):
    def get_popular(self):
        tags = map(tag_counter, super().get_queryset())
        tags = sorted(tags, key = lambda tag: tag.usage, reverse = True)
        first_five = tags[:5]
        return first_five


class Tag(models.Model):
    tag_name = models.CharField(max_length = 40, verbose_name = u"Tag", unique = True)

    objects = TagManager()

    def __str__(self):
        return self.tag_name


class QuestionManager(models.Manager):
    def get_by_tag(self, tag):
        questions = map(question_counter, super().get_queryset().filter(tags=tag))
        questions = sorted(questions, key = lambda question: question.likes, reverse = True)
        return questions

    def get_with_counters(self):
        questions = map(question_counter, super().get_queryset())
        questions = sorted(questions, key = lambda question: question.create_date, reverse = True)
        return questions

    def get_by_likes(self):
        questions = map(question_counter, super().get_queryset())
        best_questions = sorted(questions, key = lambda question: question.likes, reverse = True)
        return best_questions

    def get_hotest_questions(self):
        questions = map(question_counter, super().get_queryset())
        hotest_questions = sorted(questions, key = lambda question: question.answers, reverse = True)
        return hotest_questions


class AnswerManager(models.Manager):
    def get_answer_by_likes(self, question):
        answers = map(answer_counter, super().get_queryset().filter(question = question))
        best_answers = sorted(answers, key = lambda answer: answer.likes, reverse = True)
        return best_answers


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)

    title = models.CharField(max_length = 120, verbose_name = u"Title")
    text = models.TextField(verbose_name = u"Text of question")

    create_date = models.DateTimeField(default = datetime.now, verbose_name = u"Create time of question")

    tags = models.ManyToManyField(Tag, blank = True, db_index = True)

    is_active = models.BooleanField(default=True, verbose_name=u"Availability of question")

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)

    text = models.TextField(verbose_name = u"Text of answer")
    create_date = models.DateTimeField(default = datetime.now, verbose_name = u"Create time of answer")

    question = models.ForeignKey(Question, on_delete = models.CASCADE)

    objects = AnswerManager()



class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.CASCADE, db_index = True)

    question = models.ForeignKey(Question, on_delete = models.CASCADE, db_index = True)


class LikeToAnswer(models.Model):
    user = models.ForeignKey(Profile, on_delete = models.CASCADE)

    answer = models.ForeignKey(Answer, on_delete = models.CASCADE)
