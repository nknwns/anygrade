from django.urls import path
from .views import *

urlpatterns = [
    path('', reviews, name='home'),
    path('login', UserAuth.as_view(), name='authorization'),
    path('logout', logout_user, name='logout'),
    path('registration', UserCreate.as_view(), name='registration'),

    path('categories', categories, name='categories'),
    path('categories/<int:category_id>', categories, name='category'),
    path('categories/<int:category_id>/edit', edit_category, name='edit-category'),
    path('categories/<int:category_id>/remove', remove_category, name='remove-category'),
    path('categories/add', add_category, name='add-category'),

    path('questions', questions, name='questions'),
    path('questions/<int:question_id>', show_question, name='question'),
    path('questions/<int:question_id>/remove', remove_question, name='remove-question'),
    path('questions/add', add_question, name='add-question'),

    path('templates', templates, name='templates'),
    path('templates/<int:template_id>', show_template, name='template'),
    path('templates/<int:template_id>/edit', edit_template, name='edit-template'),
    path('templates/<int:template_id>/copy', copy_template, name='copy-template'),
    path('templates/<int:template_id>/remove', remove_template, name='remove-template'),
    path('templates/add', add_template, name='add-template'),

    path('reviews', reviews, name='reviews'),
    path('reviews/<int:review_id>', show_review, name='review'),
    path('reviews/<int:review_id>/edit', edit_review, name='edit-review'),
    path('reviews/<int:review_id>/remove', remove_review, name='remove-review'),
    path('reviews/<int:review_id>/do', do_review, name='do-review'),
    path('reviews/add', add_review, name='add-review'),

    path('staff/<slug:user_slug>', show_user, name='user')
]