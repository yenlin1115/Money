from django.shortcuts import render
from companies.models import Company
from news.models import NewsArticle
from predictions.models import Prediction

def home(request):
    context = {
        'total_companies': Company.objects.count(),
        'total_news': NewsArticle.objects.count(),
        'total_predictions': Prediction.objects.count(),
    }
    return render(request, 'home.html', context) 