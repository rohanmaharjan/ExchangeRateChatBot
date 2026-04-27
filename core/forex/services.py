from forex.models import ExchangeRate, Currency
import re
from forex.nlp_service import detect_intent_nlp

import re
from forex.models import Currency


def extract_currencies(text):
    text = text.upper()

    # Manual alias mapping
    currency_alias = {
        "DOLLAR": "USD",
        "US DOLLAR": "USD",
        "AMERICAN DOLLAR": "USD",

        "EURO": "EUR",

        "POUND": "GBP",
        "BRITISH POUND": "GBP",

        "YEN": "JPY",
        "JAPANESE YEN": "JPY",

        "RUPEE": "INR",
        "INDIAN RUPEE": "INR",

        "NEPALI RUPEE": "NPR",
        "NRS": "NPR",

        "YUAN": "CNY",
        "RENMINBI": "CNY",

        "DIRHAM": "AED",

        "RIYAL": "SAR"
    }

    found = []

    # STEP A → detect aliases first
    for alias, code in currency_alias.items():
        if alias in text and code not in found:
            found.append(code)

    # STEP B → detect actual ISO codes from DB
    db_codes = Currency.objects.values_list("iso3", flat=True)

    for code in db_codes:
        if re.search(rf"\b{code}\b", text):
            if code not in found:
                found.append(code)

    return found

def chatbot_response(user_input):
    text = user_input.lower()
    intent = detect_intent_nlp(user_input)
    currencies = extract_currencies(text)

    # Default fallback currency
    if not currencies:
        currencies = ["USD"]

    # Compare two currencies
    if intent == "compare currencies":
        if len(currencies) >= 2:
            result = compare_currencies(currencies[0], currencies[1])

            if not result:
                return "I could not find enough data to compare these currencies."

            c1 = currencies[0]
            c2 = currencies[1]

            return (
                f"Here is the information related to buy rates of {c1} and {c2} using Nepali Rupee (NRP) issued by Nepal Rastra Bank."
                f"The latest buy rate comparison shows that {c1} has a buy rate of "
                f"{result[c1]}, while {c2} has a buy rate of {result[c2]}. "
            )

        return "Please mention two currencies to compare, for example: compare USD and EUR."

    # Highest buy rate
    elif intent == "highest buy rate":
        r = highest_buy_rate()

        if not r:
            return "No exchange rate data is available at the moment."

        return (
            f"The highest recorded buy rate belongs to {r.currency.iso3}, "
            f"with a buy rate of {r.buy_rate}. "
            f"This means it is currently the strongest among the available currencies in the dataset."
        )

    # Trend
    elif intent == "currency trend":
        trend_data = list(get_trend(currencies[0]))

        if not trend_data:
            return f"No trend data found for {currencies[0]}."

        return (
            f"The trend analysis for {currencies[0]} shows how its buy rate has changed over time. "
            f"You can use this information to observe whether the currency is increasing, decreasing, "
            f"or remaining stable across different dates."
        )

    # Rate Change
    elif intent == "rate change analysis":
        result = rate_change(currencies[0])

        if not result:
            return f"Not enough data is available to calculate the rate change for {currencies[0]}."

        return (
            f"The buy rate of {currencies[0]} has changed by {result['change']:.2f}, "
            f"which represents a percentage change of {result['percent']:.2f}%. "
            f"This helps in understanding the overall movement of the currency over time."
        )
    
    # Lowest rate
    elif intent == "lowest buy rate":
        r = lowest_buy_rate()

        if not r:
            return "No exchange rate data available."

        return (
            f"The lowest recorded buy rate belongs to {r.currency.iso3}, "
            f"with a buy rate of {r.buy_rate}. "
            f"This indicates it is currently the weakest among the available currencies."
        )

    # Latest Rate
    elif intent == "latest exchange rate":
        rate = get_latest_rate(currencies[0])

        if not rate:
            return "No exchange rate data was found."

        return (
            f"The latest exchange rate for {currencies[0]} shows a buy rate of {rate.buy_rate} "
            f"and a sell rate of {rate.sell_rate} on {rate.day.date}. "
            f"This represents the most recent available forex value for that currency."
        )
    else:
        return "Sorry! Can't process the query"

    

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


# This part is replaced by nlp
'''
def detect_intent(text):
    text = text.lower()

    # Compare
    compare_keywords = [
        "compare", "difference", "vs", "versus", "between", "growth"
    ]

    # Highest
    highest_keywords = [
        "highest", "strongest", "maximum", "max", "top", "best"
    ]

    # Lowest
    lowest_keywords = [
        "lowest", "weakest", "minimum", "min", "least"
    ]

    # Change / Trend
    trend_keywords = [
        "change", "trend", "increase", "decrease",
        "history", "movement", "progress"
    ]

    # Latest Rate
    latest_keywords = [
        "latest", "current", "today", "now", "rate"
    ]

    for word in compare_keywords:
        if word in text:
            return "compare"

    for word in highest_keywords:
        if word in text:
            return "highest"

    for word in lowest_keywords:
        if word in text:
            return "lowest"

    for word in trend_keywords:
        if word in text:
            return "trend"

    for word in latest_keywords:
        if word in text:
            return "latest"

    return "unknown"
    '''