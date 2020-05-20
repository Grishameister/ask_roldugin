import re
from django import forms
from app.models import Question, Answer, Profile
from django.contrib.auth.models import User 


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data["username"]
		if ' ' in username:
			raise forms.ValidationError("Whitespaces")
		try:
			user = User.objects.filter(username=username).first
		except User.DoesNotExist:
			raise forms.ValidationError("User doesn't exist")
		return username




class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'tags']



class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['text']



class RegistrationForm(forms.Form):
	username = forms.CharField()
	email = forms.CharField()
	password = forms.CharField(min_length = 6, widget=forms.PasswordInput)
	confirm_password = forms.CharField(min_length = 6, widget=forms.PasswordInput)
	avatar = forms.ImageField(required = False)

	def clean_username(self):
		username = self.cleaned_data["username"]
		if User.objects.filter(username=username):
			raise forms.ValidationError("username exists")
		if re.search(r"\W", username):
			raise forms.ValidationError("invalid characters")
		return username

	def clean_email(self):
		email = self.cleaned_data["email"]
		if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
			raise forms.ValidationError("bad email")
		if User.objects.filter(email=email):
			raise forms.ValidationError("email has already used")
		return email

	def clean_password(self):
		password = self.cleaned_data["password"]
		if ' ' in password:
			raise forms.ValidationError("Whitespaces")

		return password

	def clean_confirm_password(self):
		confirm_password = self.cleaned_data["confirm_password"]
		password = self.cleaned_data["password"]

		if confirm_password != password:
			raise forms.ValidationError("passwords don't match")
		return confirm_password


class SettingsForm(forms.Form):
	username = forms.CharField(required=False)
	email = forms.CharField(required=False)
	password = forms.CharField(min_length=6, widget=forms.PasswordInput, required=False)
	avatar = forms.ImageField(required=False)

	def clean_password(self):
		password = self.cleaned_data["password"]
		if ' ' in password:
			raise forms.ValidationError("Whitespaces")
		return password

	def clean_username(self):
		username = self.cleaned_data["username"]
		if ' ' in username:
			raise forms.ValidationError("Whitespaces")
		try:
			user = User.objects.filter(username=username).first
		except User.DoesNotExist:
			raise forms.ValidationError("User doesn't exist")
		return username

	def clean_email(self):
		email = self.cleaned_data["email"]
		if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
			raise forms.ValidationError("bad email")
		if User.objects.filter(email=email):
			raise forms.ValidationError("email has already used")
		return email