from rest_framework import serializers
from companies.models import Company
from news.models import NewsArticle
from predictions.models import Prediction

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class NewsArticleSerializer(serializers.ModelSerializer):
    related_companies = CompanySerializer(many=True, read_only=True)
    
    class Meta:
        model = NewsArticle
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    news_article = NewsArticleSerializer(read_only=True)
    
    class Meta:
        model = Prediction
        fields = '__all__' 