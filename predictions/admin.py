from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('company', 'prediction', 'confidence_score', 'prediction_date', 'is_correct')
    search_fields = ('company__name', 'company__ticker_symbol')
    list_filter = ('prediction', 'is_correct', 'prediction_date')
