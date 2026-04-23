from forex.models import ExchangeRate

def chatbot_response(user_input):
    text = user_input.lower()
    intent = detect_intent(text)

    if intent == "compare":
        result = compare_currencies("USD", "EUR")
        return result if result else "No data available."

    elif intent == "highest":
        r = highest_buy_rate()
        if not r:
            return "No data available."
        return f"Highest: {r.currency.iso3} = {r.buy_rate}"

    elif intent == "trend":
        data = get_trend("USD")
        return [
            {"date": str(x["day__date"]), "buy_rate": x["buy_rate"]}
            for x in data
        ]

    else:
        rate = get_latest_rate("USD")
        if not rate:
            return "No data available."
        return f"USD: Buy {rate.buy_rate}, Sell {rate.sell_rate}"

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