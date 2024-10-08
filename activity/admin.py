from django.contrib import admin
from .models import Form, Section, Question, Option

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'periodicity', 'created', 'modified', 'modified_by')
    search_fields = ('name', 'slug')
    list_filter = ('periodicity', 'created', 'modified')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'form', 'order', 'created', 'modified', 'modified_by')
    search_fields = ('name',)
    list_filter = ('form', 'created', 'modified')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'section_name', 'type', 'order', 'mandatory', 'validation', 'created', 'modified', 'modified_by')
    search_fields = ('name',)
    list_filter = ('section_name', 'type', 'validation', 'created', 'modified')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_name', 'order', 'created', 'modified', 'modified_by')
    search_fields = ('text',)
    list_filter = ('question_name', 'created', 'modified')
