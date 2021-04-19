from django.shortcuts import render
from django.views import View

from app.models import Question, User, Tag

# Create your views here.

questions = [
    {
        'id': idx,
        'title': f'Title number {idx}',
        'text': f'Some text for question #{idx}'
    } for idx in range(10)
]

my_tags = [
    {
        'id': idx,
        'name': f'Tag name {idx}',
    } for idx in range(10)
]

def index(request):
    return render(request, 'index.html', {})

def ask(request):
    return render(request, 'ask.html', {})

def hot_questions(request):
    return render(request, 'hot_questions.html', {})

def login(request):
    return render(request, 'login.html', {})

def new_questions(request):
    questns = Question.objects.all().select_related()
    return render(request, 'new_questions.html', {"questions":questns})

def one_question(request, id):
    q = Question.objects.filter(pk=id)
    return render(request, 'one_question.html', {'questions': q})

def register(request):
    return render(request, 'register.html', {})

def search_tag(request, tag_name):
    tg_questions = Question.objects.filter(tags__name = tag_name) 
    return render(request, 'search_tag.html', {'questions': tg_questions, 'tag':tag_name})

def settings(request):
    return render(request, 'settings.html', {})

def popular_tags_processor(request):
    top_tags = Tag.objects.all()
    return {'popular_tags':top_tags}

def top_cats_processor(request):
    top_cats = User.objects.all()
    return {'top_cats':top_cats}
