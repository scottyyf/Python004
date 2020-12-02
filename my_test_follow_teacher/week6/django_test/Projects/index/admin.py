from django.contrib import admin
from .models import Question, Choice


# Register your models here.
# admin.site.register(Question)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ]

    inlines = [ChoiceInline]
    # fields = ['question_text', 'pub_date', ]


admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
