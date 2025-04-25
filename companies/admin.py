from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker_symbol', 'country', 'industry')
    search_fields = ('name', 'ticker_symbol')
    list_filter = ('country', 'industry')
