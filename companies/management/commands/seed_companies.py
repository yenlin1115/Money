from django.core.management.base import BaseCommand
from companies.models import Company

class Command(BaseCommand):
    help = 'Seed the database with initial companies'

    def handle(self, *args, **options):
        # US Companies
        us_companies = [
            {'name': 'Apple Inc.', 'ticker_symbol': 'AAPL', 'country': 'US', 'industry': 'Technology'},
            {'name': 'Microsoft Corporation', 'ticker_symbol': 'MSFT', 'country': 'US', 'industry': 'Technology'},
            {'name': 'Amazon.com Inc.', 'ticker_symbol': 'AMZN', 'country': 'US', 'industry': 'E-commerce'},
            {'name': 'Tesla Inc.', 'ticker_symbol': 'TSLA', 'country': 'US', 'industry': 'Automotive'},
            {'name': 'Boeing Company', 'ticker_symbol': 'BA', 'country': 'US', 'industry': 'Aerospace'},
        ]

        # Chinese Companies
        chinese_companies = [
            {'name': 'Alibaba Group', 'ticker_symbol': 'BABA', 'country': 'CN', 'industry': 'E-commerce'},
            {'name': 'Tencent Holdings', 'ticker_symbol': 'TCEHY', 'country': 'CN', 'industry': 'Technology'},
            {'name': 'Baidu Inc.', 'ticker_symbol': 'BIDU', 'country': 'CN', 'industry': 'Technology'},
            {'name': 'JD.com Inc.', 'ticker_symbol': 'JD', 'country': 'CN', 'industry': 'E-commerce'},
            {'name': 'NIO Inc.', 'ticker_symbol': 'NIO', 'country': 'CN', 'industry': 'Automotive'},
        ]

        # Taiwanese Companies
        taiwanese_companies = [
            {'name': 'Taiwan Semiconductor', 'ticker_symbol': 'TSM', 'country': 'TW', 'industry': 'Semiconductors'},
            {'name': 'Hon Hai Precision', 'ticker_symbol': 'HNHPF', 'country': 'TW', 'industry': 'Electronics'},
            {'name': 'MediaTek Inc.', 'ticker_symbol': 'MDTKF', 'country': 'TW', 'industry': 'Semiconductors'},
            {'name': 'ASE Technology', 'ticker_symbol': 'ASX', 'country': 'TW', 'industry': 'Semiconductors'},
            {'name': 'United Microelectronics', 'ticker_symbol': 'UMC', 'country': 'TW', 'industry': 'Semiconductors'},
        ]

        # Create companies
        for company_data in us_companies + chinese_companies + taiwanese_companies:
            Company.objects.get_or_create(
                ticker_symbol=company_data['ticker_symbol'],
                defaults=company_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded companies')) 