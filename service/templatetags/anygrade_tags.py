from django import template
from service.models import *

register = template.Library()


@register.inclusion_tag('anygrade/questions/table.html')
def show_questions_table(template_id=None):
    if not template_id:
        return {'questions': Question.objects.all()}
    else:
        return {'questions': Template.objects.get(pk=template_id).question.all()}


@register.inclusion_tag('anygrade/questions/table.html')
def show_questions_table_by_review(review_id):
    return {'questions': Review.objects.get(pk=review_id).question.all()}


@register.simple_tag()
def show_count_questions(group_id):
    return Template.objects.get(pk=group_id).question.count()


@register.simple_tag()
def show_count_questions_by_review(review_id):
    return Review.objects.get(pk=review_id).question.count()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_questions():
    return Question.objects.all()


@register.simple_tag()
def get_users():
    return User.objects.filter(is_staff=False)


@register.simple_tag()
def get_questions_percent(template_id):
    return Template.objects.get(pk=template_id).question.count() / 50 * 100


@register.simple_tag()
def get_questions_by_user(user_id):
    return Question.objects.filter(author_id=user_id)


@register.simple_tag()
def get_templates_by_user(user_id):
    return Template.objects.filter(author_id=user_id)

