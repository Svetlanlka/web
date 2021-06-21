from django import template
from ..models import QuestionVote, AnswerVote

register = template.Library()

@register.simple_tag
def question_liked(q, u):
    v = QuestionVote.objects.find_or_create(q, u)
    return v.vote == 1

@register.simple_tag
def question_disliked(q, u):
    v = QuestionVote.objects.find_or_create(q, u)
    return v.vote == -1

@register.simple_tag
def answer_liked(a, u):
    v = AnswerVote.objects.find_or_create(a, u)
    return v.vote == 1

@register.simple_tag
def answer_disliked(a, u):
    v = AnswerVote.objects.find_or_create(a, u)
    return v.vote == -1

@register.simple_tag
def false_tag():
    return False