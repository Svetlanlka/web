from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime

# обновление модели User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Profile(models.Model):
    name = models.CharField(max_length=255, default='None')
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    photo = models.ImageField(upload_to='img/', null=True, blank=True)
    rating = models.IntegerField(null=False,default=0)
    # login = models.CharField(max_length=255, default='None')
    # password = models.CharField(max_length=255, default='None')
    # email = models.CharField(max_length=255, default='None')
    # is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

class Question(models.Model):
    title = models.CharField(max_length=255, default=None)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='questions')
    date = models.DateField()
    tags = models.ManyToManyField('Tag', default = None)
    rating = models.ForeignKey('RatingQuestions', on_delete=models.CASCADE, default=None)
    is_like = models.BooleanField(default=False)
    is_dislike = models.BooleanField(default=False)
    answers = models.ManyToManyField('Answer', default = None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='answers')
    text = models.TextField()
    rating = models.ForeignKey('RatingAnswers', on_delete=models.CASCADE, default=None)
    is_correct = models.BooleanField(default=False)
    is_like = models.BooleanField(default=False)
    is_dislike = models.BooleanField(default=False)
    date = models.DateField(default = datetime.now, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Tag(models.Model):
    name = models.CharField(max_length=100, default=None)

    def __str__(self):
            return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class RatingAnswers(models.Model):
    rating_id = models.IntegerField(null=False, default=0)
    likes = models.IntegerField(null=False, default=0)
    dislikes = models.IntegerField(null=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.rating_id)

    class Meta:
        verbose_name = 'Рейтинг ответов'
        verbose_name_plural = 'Рейтинг ответов'

class RatingQuestions(models.Model):
    rating_id = models.IntegerField(null=False, default=0)
    likes = models.IntegerField(null=False, default=0)
    dislikes = models.IntegerField(null=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.rating_id)

    class Meta:
        verbose_name = 'Рейтинг вопросов'
        verbose_name_plural = 'Рейтинг вопросов'