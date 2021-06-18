from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from app.models import Question, Tag, Profile, Answer, QuestionVote, AnswerVote
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm, QuestionForm, AnswerForm, SettingsForm
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
    max_page = page + 4
    min_page = page - 4

    obList = paginator.get_page(page)
    return {'list': obList, "max_page": max_page, "min_page": min_page}

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

@login_required
def settings(request):
    if request.method == 'GET':
        #user_form = UserForm(instance=request.user)
        #profile_form = ProfileForm(instance=request.user.profile)
        form = SettingsForm()
    else:
        #user_form = UserForm(data=request.POST,instance=request.user)
        form = ProfileForm(
            data=request.POST,
            FILES=request.FILES,
            instance=request.user,
        )
        if form.is_valid(): #and profile_form.is_valid():
            form.save()
            #profile_form.save()
        else:
            return redirect(reverse('settings'))
        return redirect(reverse('main'))

    return render(request, 'settings.html', {'form': form})






@require_POST
def question_vote(request, question_id):
    if request.user.is_anonymous:
        return JsonResponse({'is_anonymous': True})
    opinion = str(request.POST.get('opinion'))
    question = Question.objects.find_by_id(question_id)
    vote = QuestionVote.objects.find_or_create(question, request.user)
    if opinion.lower() == 'like':
        vote.like()
    elif opinion.lower() == 'dislike':
        vote.dislike()
    else:
        return JsonResponse({'is_voted': False})
    new_question_score = question.update_score()
    question.author.profile.update_score()

    data = {
        'is_anonymous': False,
        'is_voted': True,
        'vote': vote.vote,
        'new_obj_score': new_question_score,
    }
    return JsonResponse(data)


@require_POST
def answer_vote(request):
    if request.user.is_anonymous:
        return JsonResponse({'is_anonymous': True})
    answer_id = int(request.POST.get('obj_id'))
    opinion = str(request.POST.get('opinion'))
    answer = Answer.objects.find_by_id(answer_id)
    vote = AnswerVote.objects.find_or_create(answer, request.user)
    if opinion.lower() == 'like':
        vote.like()
    elif opinion.lower() == 'dislike':
        vote.dislike()
    else:
        return JsonResponse({'is_voted': False})
    new_answer_score = answer.update_score()
    answer.author.profile.update_score()

    data = {
        'is_anonymous': False,
        'is_voted': True,
        'vote': vote.vote,
        'new_obj_score': new_answer_score,
    }

    return JsonResponse(data)