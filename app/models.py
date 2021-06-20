from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models import F


class ProfileManager(models.Manager):
    def top_five(self):
        return self.all().order_by('-rating')[:5]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    photo = models.ImageField(upload_to='avatars/', default="cat-smart.jpg")
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self, vote):
        self.rating = F('rating') + vote
        self.save()
        self.refresh_from_db()
        return self.rating

    objects = ProfileManager()

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


# отдельный класс AnswerVote, QuestionVote
# 2 Foreign key to user
class VoteInterface():
    def like(self):
        if self.vote == 1:
            self.vote = 0
        else:
            self.vote = 1
        self.save(update_fields=['vote'])
        return True

    def dislike(self):
        if self.vote == -1:
            self.vote = 0
        else:
            self.vote = -1
        self.save(update_fields=['vote'])
        return True

class VoteAnswerManager(models.Manager):
     def find_or_create(self, answer, user):
        try:
            vote = self.get(answer=answer, user=user)
        except ObjectDoesNotExist as identifier:
            vote = self.create(answer=answer, user=user)
        return vote


class AnswerVote(models.Model, VoteInterface):
    LIKE = 1
    DISLIKE = -1
    CHOICES = ((LIKE, 'like'), (DISLIKE, 'dislike'))
    ACTIONS = { x[1]: x[0] for x in CHOICES}
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='answerVotes');
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, default=None, related_name='vAnswers');
    vote = models.IntegerField(choices=CHOICES,null=False, default=0)

    def __str__(self):
        return self.user.username + ' ' + str(self.vote); 

    objects = VoteAnswerManager()

    class Meta:
        unique_together = [
            'user',
            'answer',
        ]

class VoteQuestionManager(models.Manager):
     def find_or_create(self, question, user):
        try:
            vote = self.get(question=question, user=user)
        except ObjectDoesNotExist as identifier:
            vote = self.create(question=question, user=user)
        return vote


class QuestionVote(models.Model, VoteInterface):
    LIKE = 1
    DISLIKE = -1
    CHOICES = ((LIKE, 'like'), (DISLIKE, 'dislike'))
    ACTIONS = { x[1]: x[0] for x in CHOICES}
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='questionVotes'); #liked_by
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None, related_name='vQuestions'); #blog_post
    vote = models.IntegerField(choices=CHOICES,null=False, default=0) #like

    def __str__(self):
        return self.question.title + ' ' + str(self.vote); 

    objects = VoteQuestionManager()

    class Meta:
         unique_together = [
            'user',
            'question',
        ]

class QuestionManager(models.Manager):
    def get_top(self):
        return self.all().order_by('-rating').prefetch_related('user', 'tags')

    def get_new(self):
        return self.all().order_by('-date').prefetch_related('user', 'tags')

    def get_on_tag(self, search_tag):
        questions = self.all().filter(tags__tag__iexact=search_tag).prefetch_related('user')
        if not questions:
            raise Http404
        return questions

    def get_on_id(self, new_id):
        try:
            question = self.get(pk=new_id)
        except ObjectDoesNotExist:
            raise Http404
        return question


class Question(models.Model):
    title = models.CharField(max_length=255, default=None)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='u_questions')
    date = models.DateTimeField() #datetime
    rating = models.IntegerField(default=0) #make int
    tags = models.ManyToManyField('Tag', default = None)


    def __str__(self):
        return self.title

    def update_rating(self, vote):
        self.rating = F('rating') + vote
        self.save()
        self.refresh_from_db()
        return self.rating

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class AnswerManager(models.Manager):
     def get_top(self, new_question):
        return self.filter(question=new_question).order_by('-is_correct', '-rating')

     def get_on_id(self, search_id):
        try:
            answer = self.get(pk=search_id)
        except ObjectDoesNotExist:
            raise Http404
        return answer
   

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='u_answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    date = models.DateTimeField()
    rating = models.IntegerField(default=0)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None) #Foreignkey question

    def __str__(self):
        return self.question.title + ' user: ' + self.user.username

    objects = AnswerManager()

    def update_rating(self, vote):
        self.rating = F('rating') + vote
        self.save()
        self.refresh_from_db()
        return self.rating

    def change_correct(self):
        if (self.is_correct == True):
            self.user.profile.update_rating(-1)
        else:
            self.user.profile.update_rating(1)
        self.is_correct = not self.is_correct
        self.save()
        self.refresh_from_db()
        return self.is_correct

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class TagManager(models.Manager):
    def top_ten(self):
        return self.all().order_by('-rating')[:10]

#контролировать уникальность unique
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, default=None)
    rating = models.IntegerField(default=0)

    objects=TagManager()

    def __str__(self):
        return self.name

    def set_rating(self):
        self.rating+=1

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


# обновление модели User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()