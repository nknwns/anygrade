# import simple_history
# from modeltranslation.translator import translator, TranslationOptions
# from .models import *
#
#
# @register(Question)
# class QuestionTranslationOptions(TranslationOptions):
#     fields = ('title',)
#
#
# translator.register(Question, QuestionTranslationOptions)
# simple_history.register(Question, inherit=True)
#
#
# class TemplateTranslationOptions(TranslationOptions):
#     fields = ('title', 'description')
#
#
# class CategoryTranslationOptions(TranslationOptions):
#     fields = ('title',)
#
#
# class ReviewTranslationOptions(TranslationOptions):
#     fields = ('title', 'description')
#
#
# translator.register(Question, QuestionTranslationOptions)
# translator.register(Template, TemplateTranslationOptions)
# translator.register(Category, CategoryTranslationOptions)
# translator.register(Review, ReviewTranslationOptions)
