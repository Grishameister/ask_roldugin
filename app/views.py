from django.http import HttpResponse
from django.shortcuts import render

from app.models import Question, Answer, Like, Tag, LikeToAnswer
from app.models import question_counter, answer_counter

from django.core.paginator import Paginator, InvalidPage

def paginate(object_list, request):
	paginator = Paginator(object_list, 7)
	page_number = request.GET.get('page')
	return paginator.get_page(page_number), paginator


def question(request, qid):
	try:
		question = question_counter(Question.objects.get(id = qid))
	except:
		raise Http404("No matches Questions the given query.")
	page_obj, _ = paginate(Answer.objects.get_answer_by_likes(question), request)
	tags = Tag.objects.get_popular()
	return render(request, 'question.html', {
		'question': question,
		'page_obj': page_obj,
		'tags': tags,
		})


def index(request):
	page_obj, _ = paginate(Question.objects.get_with_counters(), request)
	tags = Tag.objects.get_popular()
	return render(request, 'index.html', {
		'page_obj': page_obj,
		'tags': tags,
		})


def login(request):
	tags = Tag.objects.get_popular()
	return render(request, 'login.html', {
		'tags': tags,
		})


def signup(request):
	tags = Tag.objects.get_popular()
	return render(request, 'signup.html', {
		'tags': tags,
		})


def tag(request, tag):
	try:
		tag = Tag.objects.get(tag_name = tag)
	except:
		raise Http404("No matches Tags the given query")
	tags = Tag.objects.get_popular()
	page_obj, _ = paginate(Question.objects.get_by_tag(tag), request)
	return render(request, 'tag.html', {
		'tag': tag,
		'page_obj': page_obj,
		'tags': tags,
		})


def hot(request):
	page_obj, _ = paginate(Question.objects.get_hotest_questions(), request)
	tags = Tag.objects.get_popular()
	return render(request, 'hot.html', {
		'page_obj': page_obj,
		'tags': tags,
		})


def ask(request):
	tags = Tag.objects.get_popular()
	return render(request, 'ask.html', {
		'tags': tags,
		})
