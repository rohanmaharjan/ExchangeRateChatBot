from forex.models import ExchangeRate

def get_latest_rate(currency_code):
    return ExchangeRate.objects.filter(
        currency__iso3 = currency_code.upper()
    ).order_by("-day__date").first()


def get_rate_by_date(currency_code, date):
    return ExchangeRate.objects.filter(
        currency__iso3 = currency_code.upper(),
        day__date=date
    ).first()