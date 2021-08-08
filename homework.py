import datetime as dt


dmy = '%d.%m.%Y'


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        today_stats = sum(record.amount for record in self.records
                          if record.date == today)
        return today_stats

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        week_stats = sum(record.amount for record in self.records
                         if week_ago <= record.date <= today)
        return week_stats

    def get_today_remains(self):
        remains = self.limit - self.get_today_stats()
        return remains


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, dmy).date()


class CashCalculator(Calculator):
    USD_RATE = 73.0
    EURO_RATE = 86.0
    RUB_RATE = 1

    def get_today_cash_remained(self, currency='rub'):
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        cash_remained = self.get_today_remains()
        if cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in currencies:
            return f'Валюта {currency} не поддерживается'
        name, rate = currencies[currency]
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            message = f'На сегодня осталось {cash_remained} {name}'
        else:
            cash_remained = abs(cash_remained)
            message = (f'Денег нет, держись: твой долг - {cash_remained} '
                       f'{name}')
        return message


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.get_today_remains()
        if calories_remained > 0:
            message = (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                       f'калорийностью не более {calories_remained} кКал')
        else:
            message = 'Хватит есть!'
        return message
