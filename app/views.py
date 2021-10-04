from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from app.models import Question, Tag, Profile, Answer, QuestionVote, AnswerVote
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, QuestionForm, AnswerForm, SettingsForm
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import F

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def hot_questions(request):
    questns = Question.objects.get_top()
    questions = paginate(questns, request, 3)
    return render(request, 'hot_questions.html', {'page':questions})

def new_questions(request):
    questns = Question.objects.get_new()
    new_questions = paginate(questns, request, 3)
    print(new_questions)
    return render(request, 'new_questions.html', {'page': new_questions})

def search_tag(request, tag_name):
    filter_tg_questions = Question.objects.filter(tags__name = tag_name) 
    tg_questions = paginate(filter_tg_questions, request, 3)
    return render(request, 'search_tag.html', {'page': tg_questions, 'tag':tag_name})

def popular_tags_processor(request):
    top_tags = Tag.objects.top_ten()
    return {'popular_tags':top_tags}

def top_cats_processor(request):
    top_cats = Profile.objects.top_five()
    return {'top_cats':top_cats}

def paginate(objects_list, request, per_page = 5):
    paginator = Paginator(objects_list, per_page)
    page = int(request.GET.get('page', 1))
    max_page = page + 3
    min_page = page - 3

    obList = paginator.get_page(page)
    return {'list': obList, "max_page": max_page, "min_page": min_page}

# dz4
def login(request):
    if request.GET.get('next'):
        next_url = request.GET.get('next')
    elif request.session.get('next'):
        next_url = request.session.get('next')
    else:
        next_url = ''

    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                if next_url != '':
                    return redirect(next_url)
                else:
                    return redirect(reverse('main'))

    if request.session.get('next') != next_url:
        request.session['next'] = next_url

    return render(request, 'login.html', {'form': form})

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main'))

def register(request):
    if request.user.is_authenticated:
        raise Http404
    if request.method == 'GET':
        form = RegistrationForm()
    else:
        form = RegistrationForm(data=request.POST, FILES=request.FILES)
        if form.is_valid():
            user = form.save()
            password1 = form.cleaned_data.get('password1')
            user = auth.authenticate(
                username=user.username,
                password=password1
            )
            if user is not None:
                auth.login(request, user)
            else:
                return redirect(reverse('register'))
            return redirect(reverse('main'))
   
    return render(request, 'register.html', {'form': form})

@login_required
def ask(request):
    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST, request=request)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('one_question', kwargs={'id': question.pk}))
    return render(request, 'ask.html', {'form': form})

def one_question(request, id):
    q = Question.objects.get(pk=id)
    q2 = Answer.objects.filter(question=q)
    answers = paginate(q2, request, 3)
    context = {'question': q, 'answers': answers}

    if request.method == 'GET':
        form = AnswerForm()
    else:
        if request.user.is_authenticated:
            form = AnswerForm(data=request.POST,
                              request=request, question_id=id)
            if form.is_valid():
                answer = form.save()
                return redirect(reverse('one_question', kwargs={'id': id}) + f'#{answer.pk}')
        else:
            return redirect(reverse('login') + f'?next={request.path}')
    context['form'] = form

    return render(request, 'one_question.html', context)

# dz5
@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm()
    else:
        form = SettingsForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
        else:
            return redirect(reverse('settings'))
        return redirect(reverse('main'))

    return render(request, 'settings.html', {'form': form})


@require_POST
def answer_vote(request):
    not_login = False
    if request.user.is_anonymous:
        not_login = True
        return JsonResponse({'not_login': not_login})
    data = request.POST
    objid = data['obj_id']
    action = data['action']
    answer = Answer.objects.get_on_id(objid)
    vote = AnswerVote.objects.find_or_create(answer, request.user)
    before = vote.vote

    if (action=='like'): 
        vote.like()
    elif (action=='dislike'):
        vote.dislike()

    #v = AnswerVote.ACTIONS[action]
    v = vote.vote - before
    print('before', before)
    print('after', vote.vote)
    answer.update_rating(v)
    answer.save()
    answer.user.profile.update_rating(v)
    answer.user.profile.save()

    not_login = False
    if request.user.is_anonymous:
        not_login = True
    data = {
        'not_login': not_login,
        'vote': vote.vote,
        'vote_rating': answer.rating
    }

    return JsonResponse(data)


@require_POST
def question_vote(request, id):
    not_login = False
    if request.user.is_anonymous:
        not_login = True
        return JsonResponse({'not_login': not_login})

    data = request.POST
    objid = data['obj_id']
    action = data['action']
 
    question = Question.objects.get_on_id(objid)
    vote = QuestionVote.objects.find_or_create(question, request.user)
    before = vote.vote

    if (action=='like'): 
        vote.like()
    elif (action=='dislike'):
        vote.dislike()
    
    v = vote.vote - before
    question.update_rating(v)
    question.save()
    question.user.profile.update_rating(v)
    question.user.profile.save()

    
    data = {
        'not_login': not_login,
        'vote': vote.vote,
        'vote_rating': question.rating
    }

    return JsonResponse(data)


@require_POST
def change_correct(request):
    not_login = False
    if request.user.is_anonymous:
        not_login = True
        return JsonResponse({'not_login': not_login})

    data = request.POST
    objid = data['obj_id']

    answer = Answer.objects.get_on_id(objid)
    answer.change_correct()

    
    data = {
        'not_login': not_login,
        'is_correct': answer.is_correct,
    }
    return JsonResponse(data)