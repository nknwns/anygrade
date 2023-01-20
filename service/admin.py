import re

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import *


# Register your models here.

def get_ids(string):
    return re.findall(r'(?<=\(id:)([\d+])\)', string)


class BaseModelAdmin(SimpleHistoryAdmin, ImportExportModelAdmin):
    view_on_site = False
    save_on_top = True
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()


class TemplateResource(resources.ModelResource):
    author = fields.Field(column_name='author', attribute='author', widget=ForeignKeyWidget(User))
    question = fields.Field(column_name='question', attribute='question',
                            widget=ManyToManyWidget(Question, field='title'))

    def after_export(self, queryset, dataset, *args, **kwargs):
        objects_ = queryset.all()
        size = len(objects_)

        for i in range(size):
            data_item = list(dataset[i])
            data_item[3] = f"{objects_[i].author}(id:{objects_[i].author.pk})"

            dataset[i] = data_item
        return super().before_export(queryset, dataset, *args, **kwargs)

    def before_import_row(self, row, row_number=None, **kwargs):
        author_id = get_ids(row["author"])[0]
        row["author"] = author_id

        return super().before_import_row(row, row_number, **kwargs)

    class Meta:
        model = Template
        fields = ('id', 'title', 'description', 'author', 'question', 'updated_at', 'created_at')
        export_order = fields


class TemplateAdmin(BaseModelAdmin):
    resource_class = TemplateResource
    list_display = ('id', 'title', 'get_author', 'questions_count', 'review_count', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    list_filter = ('created_at',)
    filter_horizontal = ('question',)
    readonly_fields = ('questions_count',) + BaseModelAdmin.readonly_fields
    autocomplete_fields = ['author']

    def get_author(self, obj):
        if obj.author:
            url = reverse("admin:auth_user_change", args=(obj.author.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.author}</a>')
        return 'Без автора'

    get_author.short_description = 'Автор'


class ResultInline(admin.StackedInline):
    model = Result
    view_on_site = False


class ReviewResource(resources.ModelResource):
    author = fields.Field(column_name='author', attribute='author', widget=ForeignKeyWidget(User))
    subject = fields.Field(column_name='subject', attribute='subject', widget=ForeignKeyWidget(User))
    template = fields.Field(column_name='template', attribute='template', widget=ForeignKeyWidget(Template))
    question = fields.Field(column_name='question', attribute='question',
                            widget=ManyToManyWidget(Question))
    participant = fields.Field(column_name='participant', attribute='participant', widget=ManyToManyWidget(User))

    def after_export(self, queryset, dataset, *args, **kwargs):
        objects_ = queryset.all()
        size = len(objects_)

        for i in range(size):
            data_item = list(dataset[i])
            data_item[3] = f"{objects_[i].author}(id:{objects_[i].author.pk})"

            questions = [f"{q.title}(id:{q.pk})" for q in objects_[i].question.all()]
            data_item[6] = '; '.join(questions)

            data_item[7] = f"{objects_[i].template.title}(id:{objects_[i].template.pk})"
            data_item[8] = f"{objects_[i].subject}(id:{objects_[i].subject.pk})"

            participants = [f"{p}(id:{p.pk})" for p in objects_[i].participant.all()]
            data_item[9] = '; '.join(participants)

            dataset[i] = data_item
        return super().before_export(queryset, dataset, *args, **kwargs)

    def before_import_row(self, row, row_number=None, **kwargs):
        author_id = get_ids(row["author"])[0]
        row["author"] = author_id

        question_ids = get_ids(row["question"])
        row["question"] = ','.join(question_ids)

        template_id = get_ids(row["template"])[0]
        row["template"] = template_id

        subject_id = get_ids(row["subject"])[0]
        row["subject"] = subject_id

        participant_ids = get_ids(row["participant"])
        row["participant"] = ', '.join(participant_ids)

        return super().before_import_row(row, row_number, **kwargs)

    class Meta:
        model = Review
        fields = (
            'id', 'title', 'description', 'author', 'start_time', 'end_time', 'question', 'template', 'subject',
            'participant', 'updated_at', 'created_at')
        export_order = fields


class ReviewAdmin(BaseModelAdmin):
    resource_class = ReviewResource
    list_display = ('id', 'title', 'get_subject', 'result_count', 'question_count', 'status', 'start_time', 'end_time')
    history_list_display = ['get_subject']
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description')
    list_filter = ('created_at', 'start_time', 'end_time')
    filter_horizontal = ('question', 'participant')
    readonly_fields = ('author', 'result_count', 'status', 'question_count') + BaseModelAdmin.readonly_fields
    inlines = [ResultInline]
    autocomplete_fields = ['subject', 'template']

    def get_subject(self, obj):
        if obj.author:
            url = reverse("admin:auth_user_change", args=(obj.subject.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.subject}</a>')
        return 'Не выбран'

    get_subject.short_description = 'Опрашиваемый'


class QuestionResource(resources.ModelResource):
    author = fields.Field(column_name='author', attribute='author', widget=ForeignKeyWidget(User))
    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(Category))

    def after_export(self, queryset, dataset, *args, **kwargs):
        objects_ = queryset.all()
        size = len(objects_)

        for i in range(size):
            data_item = list(dataset[i])

            data_item[2] = f"{objects_[i].author}(id:{objects_[i].author.pk})"
            data_item[3] = f"{objects_[i].category.title}(id:{objects_[i].category.pk})"

            dataset[i] = data_item
        return super().before_export(queryset, dataset, *args, **kwargs)

    def before_import_row(self, row, row_number=None, **kwargs):
        author_id = get_ids(row["author"])[0]
        row["author"] = author_id

        category_id = get_ids(row["category"])[0]
        row["category"] = category_id

        return super().before_import_row(row, row_number, **kwargs)

    class Meta:
        model = Question
        fields = ('id', 'title', 'author', 'category', 'updated_at', 'created_at')
        export_order = fields


class QuestionAdmin(BaseModelAdmin):
    resource_class = QuestionResource
    list_display = ('id', 'title', 'get_author', 'get_category', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    list_filter = ('created_at', 'category')
    autocomplete_fields = ['author', 'category']

    def get_author(self, obj):
        if obj.author:
            url = reverse("admin:auth_user_change", args=(obj.author.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.author}</a>')
        return 'Без автора'

    def get_category(self, obj):
        if obj.category:
            url = reverse("admin:service_category_change", args=(obj.category.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.category}</a>')
        return 'Без категории'

    get_category.short_description = 'Категория'
    get_author.short_description = 'Автор'


class QuestionInline(admin.StackedInline):
    model = Question
    autocomplete_fields = ['author']
    view_on_site = False


class CategoryResource(resources.ModelResource):
    author = fields.Field(column_name='author', attribute='author', widget=ForeignKeyWidget(User, 'profile'))

    def after_export(self, queryset, dataset, *args, **kwargs):
        objects_ = queryset.all()
        size = len(objects_)

        for i in range(size):
            data_item = list(dataset[i])

            data_item[2] = f"{objects_[i].author}(id:{objects_[i].author.pk})"

            dataset[i] = data_item
        return super().before_export(queryset, dataset, *args, **kwargs)

    def before_import_row(self, row, row_number=None, **kwargs):
        author_id = get_ids(row["author"])[0]
        row["author"] = author_id

        return super().before_import_row(row, row_number, **kwargs)

    class Meta:
        model = Category
        fields = ('id', 'title', 'author', 'updated_at', 'created_at')
        export_order = fields


class CategoryAdmin(BaseModelAdmin):
    resource_class = CategoryResource
    list_display = ('id', 'title', 'get_author', 'created_at', 'get_questions_count')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    readonly_fields = ('get_questions_count',) + BaseModelAdmin.readonly_fields
    inlines = [QuestionInline]
    autocomplete_fields = ['author']

    def get_questions_count(self, obj):
        count = obj.question_set.count()
        url = (
                reverse("admin:service_question_changelist")
                + "?"
                + urlencode({"category__id__exact": f"{obj.id}"})
        )
        return mark_safe(f'{count} <a href="{url}" target="_blank">(просмотреть)</a>')

    def get_author(self, obj):
        if obj.author:
            url = reverse("admin:auth_user_change", args=(obj.author.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.author}</a>')
        return 'Без автора'

    get_author.short_description = 'Автор'
    get_questions_count.short_description = 'Количество вопросов'


class ResultResource(resources.ModelResource):
    author = fields.Field(column_name='author', attribute='author', widget=ForeignKeyWidget(User))
    subject = fields.Field(column_name='subject', attribute='subject', widget=ForeignKeyWidget(Review))

    def after_export(self, queryset, dataset, *args, **kwargs):
        objects_ = queryset.all()
        size = len(objects_)

        for i in range(size):
            data_item = list(dataset[i])

            data_item[2] = f"{objects_[i].author}(id:{objects_[i].author.pk})"
            data_item[3] = f"{objects_[i].subject.title}(id:{objects_[i].subject.pk})"

            dataset[i] = data_item
        return super().before_export(queryset, dataset, *args, **kwargs)

    def before_import_row(self, row, row_number=None, **kwargs):
        author_id = get_ids(row["author"])[0]
        row["author"] = author_id

        category_id = get_ids(row["subject"])[0]
        row["subject"] = category_id

        return super().before_import_row(row, row_number, **kwargs)

    class Meta:
        model = Result
        fields = ('id', 'data', 'author', 'subject', 'updated_at', 'created_at')
        export_order = fields


class ResultAdmin(BaseModelAdmin):
    resource_class = ResultResource
    list_display = ('id', 'subject', 'get_author', 'created_at')
    list_display_links = ('id', 'subject')
    search_fields = ('id', 'subject', 'author')
    autocomplete_fields = ['subject', 'author']

    def get_author(self, obj):
        if obj.author:
            url = reverse("admin:auth_user_change", args=(obj.author.id,))
            return mark_safe(f'<a href="{url}" target="_blank">{obj.author}</a>')
        return 'Без автора'

    get_author.short_description = 'Автор'


User.add_to_class('__str__', lambda self: f"{self.username} ({self.first_name} {self.last_name})")


class ProfileInline(admin.StackedInline):
    model = Profile
    view_on_site = False


class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    view_on_site = False


admin.site.register(Template, TemplateAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
