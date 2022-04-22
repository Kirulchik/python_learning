class Currency:
    def __init__(self, name, short):
        self.name = name
        self.short = short


class Money:
    def __init__(self, value, currency):
        self.currency = currency
        self.value = value

    def __str__(self):
        #
        return '{} {}'.format(self.value, self.currency.short)

class Convertor:
    def __init__(self, rates, name):
        self.name = name
        self.rates = rates

    # rates = {
    #     'UAH': {'USD': 20, 'EUR': 30, 'BTC': 100000},
    #     'EUR': {},
    # }
    #
    # rates['EUR']['UAH'] = 76
    # rates['EUR']['BTC'] = 234234
    def add_rate(self, currency_from, currency_to, rate):
        if currency_from.short not in self.rates:
            self.rates[currency_from.short] = {}
        self.rates[currency_from.short][currency_to.short] = rate

    # Money(20, Currency('grivna', 'UAH')), Currency('euro', 'EUR') -> Money(money.value*rate, Currency('euro', 'EUR'))
    def convert(self, money, currency):
        if currency.short in self.rates:
            if money.currency.short in self.rates[currency.short]:
                rate = self.rates[currency.short][money.currency.short]
                return Money(money.value/rate, currency)

        return money







grn = Currency('grivna', 'UAH')
grn2 = Currency('grivna', 'UAH')
grn == grn2

eur = Currency('euro', 'EUR')
usd = Currency('dollar', 'USD')
btc = Currency('bitcoin', 'BTC')
budget = Money(20000, grn)

bank = Convertor({}, 'Kirill')
bank.add_rate(eur, grn, 30)
bank.add_rate(usd, grn, 27)
bank.add_rate(btc, grn, 50000)
bank.add_rate(usd, eur, 0.9)

eur_budget = bank.convert(budget, eur)
usd_budget = bank.convert(budget, usd)
btc_budget = bank.convert(budget, btc)
print(eur_budget)
print(usd_budget)
print(btc_budget)





# dict = {}
# dict['sdf'] = 3
# dict['adgd'] = 436
# print(dict['sdf'])
#
# dict2 = {2: 2, 35: 35, 215: 535}
# dict2[64] = 46
# print(34 in dict2)
# print(dict2[215])
#
# arr = []
# arr.append('dsgs')
# arr.append('dsgsdg')
# arr.append('cxvt')
# print(arr)
# print(dict)



# a = {'b': {'c': {'d': {'f': {'x': 1}}}}}
# a['b']['c']['d']['f']['x'] = 2
# print(a['b']['c']['d']['f']['x'])
#
#
#
# rates = {
#     'UAH': {'USD': 20, 'EUR': 30, 'BTC': 100000},
#     'EUR': {},
# }
#
# if 'USD' not in rates:
#     rates['USD'] = {}
# rates['USD']['UAH'] = 40
# rates['EUR']['USD'] = 76
# rates['EUR']['BTC'] = 234234
# print(rates)
