from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article, Tag, Scope


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        rez = 0
        for form in self.forms:
            if len(form.cleaned_data) != 0:
                if form.cleaned_data['is_main'] == True:
                    rez += 1
            if rez > 1:
                raise ValidationError('Основным может быть только один раздел')
            elif rez == 0:
                raise ValidationError('Укажите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 3
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name',]



