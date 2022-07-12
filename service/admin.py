from django.contrib import admin

# Register your models here.

from .models import *


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    list_filter = ('created_at', )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_time', 'end_time', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description')
    list_filter = ('created_at', 'start_time', 'end_time')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    list_filter = ('created_at', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'author', 'created_at')
    list_display_links = ('id', 'subject')
    search_fields = ('id', 'subject', 'author')


admin.site.register(Template, TemplateAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Result, ResultAdmin)