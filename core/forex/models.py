from django.db import models

class Currency(models.Model):
    iso3 = models.CharField(max_length=10, unique=True)  # USD, INR, NPR
    name = models.CharField(max_length=100)              # U.S. Dollar
    unit = models.IntegerField(default=1)                # 1, 100

    def __str__(self):
        return self.iso3
    
class ExchangeRateDay(models.Model):
    date = models.DateField(unique=True)
    published_on = models.DateTimeField()

    def __str__(self):
        return str(self.date)
    
class ExchangeRate(models.Model):
    day = models.ForeignKey(ExchangeRateDay, on_delete=models.CASCADE, related_name="rates")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    buy_rate = models.FloatField()
    sell_rate = models.FloatField()

    class Meta:
        unique_together = ('day', 'currency')  # prevents duplicates

    def __str__(self):
        return f"{self.currency.iso3} - {self.day.date}"
