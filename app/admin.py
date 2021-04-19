from django.contrib import admin

# Register your models here.
from app.models import User, Question, Answer, Tag, RatingAnswers, RatingQuestions

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(RatingAnswers)
admin.site.register(RatingQuestions)
