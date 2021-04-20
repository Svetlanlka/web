from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views import View

from app.models import Question, Tag, Profile
from django.contrib.auth.models import User

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
    questns = Question.objects.all().select_related()
    questions = paginate(questns, request, 3)
    return render(request, 'hot_questions.html', {'questions':questions})

def login(request):
    return render(request, 'login.html', {})

def new_questions(request):
    questns = Question.objects.all().select_related()
    new_questions = paginate(questns, request, 3)
    return render(request, 'new_questions.html', {'questions': new_questions})

def one_question(request, id):
    q = Question.objects.get(pk=id)
    q2 = q.answers.all()
    answers = paginate(q2, request, 3)
    return render(request, 'one_question.html', {'question': q, 'answers': answers})

def register(request):
    return render(request, 'register.html', {})

def search_tag(request, tag_name):
    filter_tg_questions = Question.objects.filter(tags__name = tag_name) 
    tg_questions = paginate(filter_tg_questions, request, 3)
    return render(request, 'search_tag.html', {'questions': tg_questions, 'tag':tag_name})

def settings(request):
    return render(request, 'settings.html', {})

def popular_tags_processor(request):
    top_tags = Tag.objects.all()
    return {'popular_tags':top_tags}

def top_cats_processor(request):
    top_cats = Profile.objects.all()
    return {'top_cats':top_cats}

def paginate(objects_list, request, per_page = 5):
    paginator = Paginator(objects_list, per_page)
    page = int(request.GET.get('page', 1))
    max_page = page + 2
    min_page = page - 2

    questions_list = paginator.get_page(page)
    return {'questions_list': questions_list, "max_page": max_page, "min_page": min_page}
