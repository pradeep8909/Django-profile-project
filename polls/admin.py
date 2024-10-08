from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text", "status"],}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    list_display = ["id","question_text", "pub_date", "was_published_recently","status"]
    list_filter = ["pub_date"]
    search_fields = ["question_text", "id"]

    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)