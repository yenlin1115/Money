from django.contrib import admin
from .models import NewsArticle

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_date', 'sentiment_score')
    search_fields = ('title', 'content')
    list_filter = ('source', 'published_date')
    filter_horizontal = ('related_companies',)
