import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from forex.models import Currency, ExchangeRateDay, ExchangeRate

class Command(BaseCommand):
    help = "Import forex data from CSV"

    def handle(self, *args, **kwargs):
        with open("forex_data.csv", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:

                currency_obj, _ = Currency.objects.update_or_create(
                    iso3=row["Currency_iso3"],
                    defaults={
                        "name": row["Currency_Name"],
                        "unit": int(row["Unit"])
                    }
                )

                day_obj, _ = ExchangeRateDay.objects.get_or_create(
                    date=datetime.strptime(row["Date"], "%Y-%m-%d").date(),
                    defaults={
                        "published_on": datetime.fromisoformat(row["Published_Date"])
                    }
                )

                ExchangeRate.objects.update_or_create(
                    day=day_obj,
                    currency=currency_obj,
                    defaults={
                        "buy_rate": float(row["Buy_Rate"]),
                        "sell_rate": float(row["Sell_Rate"])
                    }
                )

        self.stdout.write(self.style.SUCCESS("CSV Imported Successfully"))