from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, NewsArticleViewSet, PredictionViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'news', NewsArticleViewSet)
router.register(r'predictions', PredictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 