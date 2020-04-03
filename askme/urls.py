from django.http import HttpResponse
from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('question/<int:qid>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag>', views.tag, name = 'tag'),
    path('hot/', views.hot, name='hot'),
    path('signup/', views.signup, name='signup'),
]
