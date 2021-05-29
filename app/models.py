from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django.db.models import Sum

# обновление модели User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Profile(models.Model):
    # name убрать
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    photo = models.ImageField(upload_to='img/', null=True, blank=True)
    rating = models.IntegerField(null=False,default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

class QuestionManager(models.Manager):
    def get_top(self):
        return self.all().order_by('-rating').prefetch_related('user', 'tags')

    def get_new(self):
        return self.all().order_by('-date').prefetch_related('user', 'tags')

    def get_on_tag(search_tag):
        questions = self.all().filter(tags__tag__iexact=search_tag).prefetch_related('user')
        if not questions:
            raise Http404
        return questions

    def get_on_id(new_id):
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
    tags = models.ManyToManyField('Tag', default = None)
    rating = models.IntegerField(null=False, default=0) #make int
    # delete is_like
    # delete is_dislike
    # delete answers

    def __str__(self):
        return self.title

    def update_score(self):
        vsum = self.vQuestions.aggregate(Sum('vote'))
        self.rating = vsum['vote__sum']
        self.save(update_fields=['rating'])
        return self.rating

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class AnswerManager(models.Manager):
     def get_top(self, new_question):
        return self.filter(question=new_question).order_by('-is_correct', '-score')

     def get_on_id(self, search_id):
        try:
            answer = self.get(pk=search_id)
        except ObjectDoesNotExist:
            raise Http404
        return answer
   

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='u_answers')
    text = models.TextField()
    rating = models.IntegerField(null=False, default=0)
    is_correct = models.BooleanField(default=False)
    date = models.DateTimeField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None) #Foreignkey question

    def __str__(self):
        return self.question.title + ' user: ' + self.user.username

    def update_score(self):
        vsum = self.vAnswers.aggregate(Sum('vote'))
        self.rating = vsum['vote__sum']
        self.save(update_fields=['rating'])
        return self.rating

    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

#контролировать уникальность unique
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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

class AnswerVote(models.Model, VoteInterface):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='answerVotes');
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, default=None, related_name='vAnswers');
    vote = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.user.username + ' ' + str(self.vote); 

    def find_or_create(self, answer, user):
        try:
            vote = self.get(answer=answer, user=user)
        except ObjectDoesNotExist as identifier:
            vote = self.create(answer=answer, user=user)
        return vote

    class Meta:
        unique_together = [
            'user',
            'answer',
        ]


class QuestionVote(models.Model, VoteInterface):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='questionVotes'); #liked_by
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None, related_name='vQuestions'); #blog_post
    vote = models.IntegerField(null=False, default=0) #like

    def __str__(self):
        return self.question.title + ' ' + str(self.vote); 

    def find_or_create(self, question, user):
        try:
            vote = self.get(question=question, user=user)
        except ObjectDoesNotExist as identifier:
            vote = self.create(question=question, user=user)
        return vote

    class Meta:
         unique_together = [
            'user',
            'question',
        ]
    
    


# class RatingAnswers(models.Model):
#     rating_id = models.IntegerField(null=False, default=0)
#     likes = models.IntegerField(null=False, default=0)
#     dislikes = models.IntegerField(null=True, default=0)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

#     def __str__(self):
#         return str(self.likes - self.dislikes)

#     def get_rating(self):
#         return self.likes - self.dislikes

#     class Meta:
#         verbose_name = 'Рейтинг ответов'
#         verbose_name_plural = 'Рейтинг ответов'

# class RatingQuestions(models.Model):
#     rating_id = models.IntegerField(null=False, default=0)
#     likes = models.IntegerField(null=False, default=0)
#     dislikes = models.IntegerField(null=True, default=0)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

#     def __str__(self):
#         return str(self.likes - self.dislikes)
    
#     def get_rating(self):
#         return self.likes - self.dislikes

#     class Meta:
#         verbose_name = 'Рейтинг вопросов'
#         verbose_name_plural = 'Рейтинг вопросов'