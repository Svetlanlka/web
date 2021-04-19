from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255, default='None')
    login = models.CharField(max_length=255, default='None')
    password = models.CharField(max_length=255, default='None')
    email = models.CharField(max_length=255, default='None')
    photo = models.ImageField(upload_to='img/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Question(models.Model):
    title = models.CharField(max_length=255, default=None)
    text = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    date = models.DateField()
    tags = models.ManyToManyField('Tag', default = None)
    rating = models.ForeignKey('RatingQuestions', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    user = models.ForeignKey('Question', on_delete=models.CASCADE, default=None)
    text = models.TextField()
    rating = models.ForeignKey('RatingAnswers', on_delete=models.CASCADE, default=None)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

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
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.rating_id)

    class Meta:
        verbose_name = 'Рейтинг ответов'
        verbose_name_plural = 'Рейтинг ответов'

class RatingQuestions(models.Model):
    rating_id = models.IntegerField(null=False, default=0)
    likes = models.IntegerField(null=False, default=0)
    dislikes = models.IntegerField(null=True, default=0)
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.rating_id)

    class Meta:
        verbose_name = 'Рейтинг вопросов'
        verbose_name_plural = 'Рейтинг вопросов'