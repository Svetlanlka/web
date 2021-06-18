from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from django.db import models
from .models import Question, Answer, User, Profile
from django.core.exceptions import ValidationError
import datetime

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

    class Meta:
        model = User
        fields = ('username', 'password1',
                  'password2', 'email', 'photo')

class UserForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Enter new login', max_length=256)
    email = forms.EmailField(required=True, label='Enter new email', max_length=256)

    def save(self, *args, **kwargs):
        user = super(UserForm, self).save(*args, **kwargs)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(required=True, label='Choose new photo', widget=forms.FileInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.FILES = kwargs.pop('FILES', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        profile = super(ProfileForm, self).save(*args, **kwargs)
        profile.user = self.user
        profile.photo = self.cleaned_data['photo']
        profile.save()
        print(profile.photo)
        return profile

    class Meta:
        model = Profile
        fields = ('photo',)


class SettingsForm(forms.ModelForm):
    photo = forms.ImageField(required=True, label='Choose new photo', widget=forms.FileInput())

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.profile.photo = self.cleaned_data['photo']
        user.profile.save()
        return user

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