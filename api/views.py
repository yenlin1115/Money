from django.shortcuts import render
from rest_framework import viewsets
from companies.models import Company
from news.models import NewsArticle
from predictions.models import Prediction
from .serializers import CompanySerializer, NewsArticleSerializer, PredictionSerializer

# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
