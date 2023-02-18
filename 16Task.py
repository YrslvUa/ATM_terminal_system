import requests
from bs4 import BeautifulSoup as Bs
from datetime import datetime


class Menu:
    def __init__(self):
        UserVerification.pin_code_verification()

    @staticmethod
    def menu():
        while True:
            try:
                first = int(input('''What you want?
                \r1.Get Money\n2.ReplenishBalance\n3.ExchangeRate\n4.CurrencyExchange
                \rPrint number:\n'''))
                if first == 1:
                    GetMoney()
                elif first == 2:
                    ReplenishBalance()
                elif first == 3:
                    ExchangeRate()
                elif first == 4:
                    CurrencyExchange()
                else:
                    print('Try again!')
            except ValueError:
                print('Try again!')

    @staticmethod
    def update_menu():
        while True:
            try:
                a = int(input('You want end cod(1) or call menu(2):\n'))
                if a == 1:
                    print("Don't forget your card)")
                    exit()
                elif a == 2:
                    Menu.menu()
                else:
                    print('Try again!')
            except ValueError:
                print('Try again!')

    @staticmethod
    def data_and_time(name):
        with open('OperationTime.txt', 'a', encoding='utf-8') as file:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S.%d/%m/%Y ")
            new_dct = {key: value for key, value in zip(dt_string.split(), name.split())}
            file.write(f'{str(new_dct)}\n')


class UserVerification:
    name_user = None

    @staticmethod
    def pin_code_verification():
        while True:
            with open('UserData.txt', 'r', encoding='utf-8') as UserData:
                name_user = input('Print your name.\nFor example as: User_(Your number from 1 to 9)\n')
                for line in UserData:
                    if name_user in line.split():
                        i = 0
                        n = 3
                        while i < 3:
                            pin_code_user = input('Print your pin code:\n')
                            if pin_code_user in line.split():
                                print('Successful access!')
                                UserVerification.name_user = name_user
                                Menu.menu()
                            else:
                                i += 1
                                n -= 1
                                print(f'Your have {n} attempts.')
                        else:
                            raise ValueError('Wrong pin code. Your card is blocked.')
                else:
                    print("Can't recognize the card. Try again!")


class AboutUserAndSystemBalance(UserVerification):
    user_balance = None
    sys_balance = None

    def __init__(self):
        self.account_balance()
        self.system_balance()
        super().__init__()

    def account_balance(self):
        with open('UserBalance.txt', 'r', encoding='utf-8') as UserBalance:
            for line in UserBalance:
                if self.name_user in line.split():
                    self.user_balance = line.split()[2]
                    return self.user_balance

    def system_balance(self):
        with open('SystemBalance.txt', 'r', encoding='utf-8') as SystemBalance:
            number = SystemBalance.readlines()
            for line in number:
                for i in line.split():
                    if i.isdigit():
                        self.sys_balance = i

    def money(self, some_money, sign):
        if sign == '-':
            self._new_user_balance = int(self.user_balance) - some_money
            self._new_system_balance = int(self.sys_balance) - some_money
        elif sign == '+':
            self._new_user_balance = int(self.user_balance) + some_money
            self._new_system_balance = int(self.sys_balance) + some_money
        new_line = str(f'{self.name_user} : {self._new_user_balance}')
        with open('SystemBalance.txt', 'w', encoding='utf-8') as f:
            f.write(str(self._new_system_balance))
        with open('UserBalance.txt', 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if self.name_user in line:
                    pos = i
        with open('UserBalance.txt', 'r', encoding='utf-8') as f:
            L = f.readlines()
            if (pos >= 0) and (pos < len(L)):
                if pos == len(L) - 1:
                    L[pos] = new_line
                else:
                    L[pos] = new_line + '\n'
        with open('UserBalance.txt', 'w', encoding='utf-8') as f:
            for line in L:
                f.write(line)
        Menu.update_menu()


class GetMoney(AboutUserAndSystemBalance):
    def __init__(self):
        self.money = None
        self.get_money()
        super().__init__()

    def get_money(self, money=None):
        if money:
            self._money = money
        else:
            while True:
                try:
                    self._money = int(input('How much money do you want to get?:\n'))
                    break
                except ValueError:
                    print('Try again!')
        self.account_balance(), self.system_balance()
        if self._money <= (int(self.user_balance) and int(self.sys_balance)):
            Menu.data_and_time('GetMoney')
            print('Take your money...')
            super().money(some_money=self._money, sign='-')
        elif self._money > int(self.user_balance):
            print('There is not enough money on the card!')
        elif self._money > int(self.sys_balance):
            print('Sorry, but the ATM has no money to dispense((')


class ReplenishBalance(AboutUserAndSystemBalance):
    def __init__(self):
        self.money = int(input('Enter the top_up amount:\n'))
        self.replenish_balance()
        super().__init__()

    def replenish_balance(self):
        self.account_balance(), self.system_balance()
        Menu.data_and_time('ReplenishBalance')
        print(f'The balance was successfully replenished.')
        super().money(some_money=self.money, sign='+')


class ExchangeRate:
    def __init__(self):
        self.exchange_rate()

    def exchange_rate(self):
        url = 'https://bank.gov.ua/ua/markets/exchangerates'

        response = requests.get(url)
        html = Bs(response.content, 'html.parser')
        code = [i.find_all('td', {'data-label': 'Код літерний'}) for i in html.select('#exchangeRates')][0]
        exchange_rate = [i.find_all('td', {'data-label': 'Офіційний курс'}) for i in html.select('#exchangeRates')][0]
        self.new_dict = {key.text: value.text for key, value in zip(code, exchange_rate)}
        Menu.data_and_time('ExchangeRate')
        for i, (k, v) in enumerate(self.new_dict.items(), start=1):
            print(f'{i}. {k}:{v}')


class CurrencyExchange(ExchangeRate, GetMoney):
    def __init__(self):
        self.currency_exchange()
        super().__init__()

    def currency_exchange(self):
        self.exchange_rate(), self
        while True:
            try:
                num_cur = int(input(f'Write the number of the currency you want to receive:\n'))
                for i, (key, value) in enumerate(self.new_dict.items(), start=1):
                    if i == num_cur:
                        while True:
                            try:
                                how_many = int(input(f'How much do you want to get {key}:\n'))
                                uah = how_many * float(value.replace(",", '.'))
                                with open('UserForeignCurrencies.txt', 'a', encoding='utf-8') as UFC:
                                    UFC.write(str(f'{key} : {how_many}\n'))
                                Menu.data_and_time('CurrencyExchange')
                                super().get_money(money=int(uah))
                            except ValueError:
                                print('Try again!')
            except ValueError:
                print('Try again!')


Menu()
