from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse

from app.models import Question, Answer, Like, Tag, LikeToAnswer, Profile
from app.models import question_counter, answer_counter

from app.forms import RegistrationForm, LoginForm, AnswerForm, QuestionForm, SettingsForm

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required

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

	if request.method == 'POST':
		form = AnswerForm(data=request.POST)
		if form.is_valid() and request.user.is_authenticated:
			answer = Answer.objects.create(author=request.user.profile, 
									text=form.cleaned_data['text'],
									question=question)
	else:
		form = AnswerForm()
	page_obj, _ = paginate(Answer.objects.get_answer_by_likes(question), request)
	tags = Tag.objects.get_popular()
	return render(request, 'question.html', {
		'user': request.user,
		'form': form,
		'question': question,
		'page_obj': page_obj,
		'tags': tags,
		})


def index(request):
	page_obj, _ = paginate(Question.objects.get_with_counters(), request)
	tags = Tag.objects.get_popular()
	return render(request, 'index.html', {
		'user': request.user,
		'page_obj': page_obj,
		'tags': tags,
		})	


def login(request):
	if request.method == 'GET':
		form = LoginForm()
	else:
		form = LoginForm(data=request.POST)
		if form.is_valid():
			user = auth.authenticate(request, **form.cleaned_data)
			if user is not None:
				auth.login(request, user)
				return redirect('/index')
	tags = Tag.objects.get_popular()
	return render(request, 'login.html', {
		'user': request.user,
		'form': form,
		'tags': tags,
		})


def signup(request):
	tags = Tag.objects.get_popular()
	if request.method == 'GET':
		form = RegistrationForm()
	else:
		form = RegistrationForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			user = User.objects.create_user(
				form.cleaned_data["username"],
				form.cleaned_data["email"],
				form.cleaned_data["password"])
			Profile.objects.create(user=user)
			return redirect('/login')

	return render(request, 'signup.html', {
		'form': form,
		'tags': tags,
		})


def tag(request, tag):
	try:
		tag = Tag.objects.get(tag_name=tag)
	except:
		raise Http404("No matches Tags the given query")
	tags = Tag.objects.get_popular()
	page_obj, _ = paginate(Question.objects.get_by_tag(tag), request)
	return render(request, 'tag.html', {
		'user': request.user,
		'tag': tag,
		'page_obj': page_obj,
		'tags': tags,
		})


def hot(request):
	page_obj, _ = paginate(Question.objects.get_hotest_questions(), request)
	tags = Tag.objects.get_popular()
	return render(request, 'hot.html', {
		'user': request.user,
		'page_obj': page_obj,
		'tags': tags,
		})


@login_required
def ask(request):
	tags = Tag.objects.get_popular()
	if request.method == "GET":
		form = QuestionForm()
	else:
		form = QuestionForm(data=request.POST)
		if form.is_valid():
			question = Question.objects.create(author=request.user.profile,
										title=form.cleaned_data['title'],  
										text=form.cleaned_data["text"])
			return redirect(reverse('question', kwargs={'qid': question.pk}))

	return render(request, 'ask.html', {
		'form': form,
		'user': request.user,
		'tags': tags,
		})


@login_required
def profile(request):
	tags = Tag.objects.get_popular()
	if request.method == "GET":
		form = SettingsForm()
	else:
		form = SettingsForm(data=request.POST)

		
	return render(request, 'profile.html', {
		'form': form,
		'user': request.user,
		'tags': tags,
		})


@login_required
def logout_view(request):
	logout(request)
	return redirect(request.META.get('HTTP_REFERER', '/'))