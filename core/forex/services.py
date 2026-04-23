from forex.models import ExchangeRate
import re
from forex.models import Currency

def extract_currencies(text):
    # get all ISO codes from DB
    codes = Currency.objects.values_list("iso3", flat=True)

    found = []

    for code in codes:
        if re.search(rf"\b{code}\b", text.upper()):
            found.append(code)

    return found

def chatbot_response(user_input):
    text = user_input.lower()

    intent = detect_intent(text)
    currencies = extract_currencies(text)

    # DEFAULT fallback currency
    if not currencies:
        currencies = ["USD"]

    # COMPARE
    if intent == "compare":
        if len(currencies) >= 2:
            return str(compare_currencies(currencies[0], currencies[1]))
        else:
            return "Please mention 2 currencies to compare (e.g. USD EUR)"

    # HIGHEST
    elif intent == "highest":
        r = highest_buy_rate()
        if not r:
            return "No data available."
        return f"Highest: {r.currency.iso3} = {r.buy_rate}"

    # TREND
    elif intent == "trend":
        return list(get_trend(currencies[0]))

    # RATE CHANGE
    elif "change" in text:
        return rate_change(currencies[0])

    # DEFAULT (latest rate)
    else:
        rate = get_latest_rate(currencies[0])
        if not rate:
            return "No data found."

def get_latest_rate(currency_code):
    return ExchangeRate.objects.filter(
        currency__iso3=currency_code.upper()
    ).order_by("-day__date").first()


def get_rate_by_date(currency_code, date):
    return ExchangeRate.objects.filter(
        currency__iso3=currency_code.upper(),
        day__date=date
    ).first()


def compare_currencies(c1, c2):
    r1 = get_latest_rate(c1)
    r2 = get_latest_rate(c2)

    if not r1 or not r2:
        return None

    return {
        c1: r1.buy_rate,
        c2: r2.buy_rate
    }


def highest_buy_rate():
    return ExchangeRate.objects.order_by("-buy_rate").first()


def lowest_buy_rate():
    return ExchangeRate.objects.order_by("buy_rate").first()


def rate_change(currency):
    rates = ExchangeRate.objects.filter(
        currency__iso3=currency
    ).order_by("day__date")

    if rates.count() < 2:
        return None

    first = rates.first().buy_rate
    last = rates.last().buy_rate

    if first == 0:
        return None

    return {
        "change": last - first,
        "percent": ((last - first) / first) * 100
    }


def get_trend(currency):
    return ExchangeRate.objects.filter(
        currency__iso3=currency
    ).order_by("day__date").values("day__date", "buy_rate")

def detect_intent(text):
    text = text.lower()

    if "compare" in text:
        return "compare"

    if "highest" in text:
        return "highest"

    if "change" in text or "trend" in text:
        return "trend"

    return "latest"