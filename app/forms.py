from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from django.db import models
from .models import Question, Answer, User, Profile
from django.core.exceptions import ValidationError
import datetime
import re

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Enter email', max_length=256)
    photo = forms.ImageField(required=False, label='Choose photo', widget=forms.FileInput())

    def __init__(self, *args, **kwargs):
        self.FILES = kwargs.pop('FILES', None)
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        user = super(RegistrationForm, self).save(*args, **kwargs)
        user.refresh_from_db()
        if (self.FILES['photo']):
            user.profile.photo = self.FILES['photo']
        user.profile.save()
        user.email = self.cleaned_data['email']
        user.save()
        return user 

    class Meta:
        model = User
        fields = ('username', 'password1',
                  'password2', 'email', 'photo')


class SettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Enter email', max_length=256)
    photo = forms.ImageField(required=True, label='Choose new photo', widget=forms.FileInput())

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.photo = self.cleaned_data['photo']
        user.profile.save()
        return user

    def clean(self):
        data = super().clean()

        name = data['username']
        if re.fullmatch('^([a-z]|[A-Z])+\S+$', name) is None:
            self.add_error(
                'username',
                'Start your nickname with letter and do not use whitespace-characters'
            )
            
        # email = data['email']
        # if re.fullmatch('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email) is None:
        #     self.add_error('email', 'Email is not valid')

    class Meta:
        model = User
        fields = ('username', 'email', 'photo')

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(QuestionForm, self).__init__(*args, **kwargs)

    def save(self):
        question = super(QuestionForm, self).save(commit=False)
        question.user = self.request.user
        question.date = datetime.datetime.now()
        question.save()
        question.tags.set(self.request.POST.getlist('tags'))
        question.save()
        return question

    def clean(self):
        data = super().clean()
        title = data['title']
        if re.fullmatch('^([a-z]|[A-Z])+[^\n\t\r]+$', title) is None:
            self.add_error('title', 'Title start with letter or contains wrong symbols')

        tags = data['tags']
        if len(tags) > 5:
            self.add_error('tags', 'You can choose up to 5 tags')

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags',)

class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.question_id = kwargs.pop('question_id', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self):
        answer = super(AnswerForm, self).save(commit=False)
        answer.user = self.request.user
        answer.question = Question.objects.get_on_id(self.question_id)
        answer.date = datetime.datetime.now()
        answer.save()
        return answer

    class Meta:
        model = Answer
        fields = ('text',)