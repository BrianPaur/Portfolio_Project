import finnhub
import pandas as pd
import sqlite3
from datetime import date
from settings import api_key

###############################################################
#### Creates db that houses Portfolio and Transaction data ####
####      Uses finnhub api to pull down security data      ####
###############################################################

class Portfolio:

    def __init__(self, port = None, apisetup = None):
        self.port = port
        self.apisetup = apisetup

    def holdings(self):
        # establishes db connection
        connection = self.port
        cursor = connection.cursor()

        # tries to create portfolio table is none exists
        try:
            cursor.execute(
                "CREATE TABLE port (ticker TEXT UNIQUE, quantity INTEGER, price INTEGER, market_value INTEGER)")
        except:
            pass

        # prints out db in table form
        # returns empty table if no data points
        df = pd.read_sql_query("SELECT * FROM port", connection)
        print(df)

    def transactions(self):
        # establishes db connection
        connection = self.port
        cursor = connection.cursor()

        # tries to create transaction table is none exists
        try:
            cursor.execute(
                "CREATE TABLE trans (date TEXT, ticker TEXT, quantity INTEGER, price INTEGER, net_cash INTEGER)")
        except:
            pass

        df = pd.read_sql_query("SELECT * FROM trans", connection)
        print(df)

    def deposit_cash(self, amount):
        # establishes db connection
        connection = self.port
        cursor = connection.cursor()
        try:
            old_balance = cursor.execute("SELECT quantity FROM port WHERE ticker = ?", ('CASH',)).fetchone()[0]
            new_balance = amount + old_balance
            cursor.execute("UPDATE port SET quantity = ?, price = ?, market_value = ? WHERE ticker = ?", (new_balance, 100, new_balance, 'CASH'))
            cursor.execute("INSERT INTO trans VALUES (?, ?, ?, ?, ?)", (date.today().strftime("%m/%d/%y"), 'CASH', amount, 100, amount))

        except:
            cursor.execute("INSERT INTO port VALUES (?, ?, ?, ?)", ('CASH', amount, 100, amount))
            cursor.execute("INSERT INTO trans VALUES (?, ?, ?, ?, ?)",(date.today().strftime("%m/%d/%y"), 'CASH', amount, 100, amount))

        # saves and closes out connection to db
        connection.commit()
        cursor.close()

    def withdraw_cash(self, amount):
        # establishes db connection
        connection = self.port
        cursor = connection.cursor()

        old_balance = cursor.execute("SELECT quantity FROM port WHERE ticker = ?", ('CASH',)).fetchone()[0]

        if old_balance - amount < 0:
            print('insufficient funds')
        elif cursor.execute("SELECT quantity FROM port WHERE ticker = ?", ('CASH',)).fetchone()[0] == None:
            print('no cash holdings')
        else:
            old_balance = cursor.execute("SELECT quantity FROM port WHERE ticker = ?", ('CASH',)).fetchone()[0]
            new_balance = old_balance - amount
            cursor.execute("UPDATE port SET quantity = ?, market_value = ? WHERE ticker = ?", (new_balance, new_balance, 'CASH'))
            cursor.execute("INSERT INTO trans VALUES (?, ?, ?, ?, ?)", (date.today().strftime("%m/%d/%y"), 'CASH', (amount*-1), 100, (amount*-1)))

        # saves and closes out connection to db
        connection.commit()
        cursor.close()

    def buy(self, ticker, qty):
        # establishes db connection
        connection = self.port
        cursor = connection.cursor()

        price = self.apisetup.quote(ticker.upper())['c']
        net_amount = price * qty
        cash_bal = cursor.execute("SELECT quantity FROM port WHERE ticker = ?", ('CASH',)).fetchone()[0]

        if price == 0:
            print("security doesn't exist")
        else:
            if cash_bal > net_amount:

                try:

                    # tries to update amount on the portfolio table and updates transaction table
                    old_balance = cursor.execute("SELECT quantity FROM port WHERE ticker = ?", (ticker.upper(),)).fetchone()[0]
                    new_balance = qty + old_balance
                    new_market_value = new_balance * price
                    new_cash_balance = cash_bal - net_amount
                    cursor.execute("UPDATE port SET quantity = ?, price = ?,  market_value = ? WHERE ticker = ?", (new_balance, price, new_market_value, ticker.upper()))
                    cursor.execute("UPDATE port SET quantity = ?, price = ?,  market_value = ? WHERE ticker = ?", (new_cash_balance, 100, new_cash_balance, 'CASH'))
                    cursor.execute("INSERT INTO trans VALUES (?, ?, ?, ?, ?)",(date.today().strftime("%m/%d/%y"), ticker.upper(), qty, price, net_amount))
                except:

                    # if doesn't exists adds it to portfolio table and updates transaction table
                    market_value = qty * price
                    new_cash_balance = cash_bal - net_amount
                    cursor.execute("INSERT INTO port VALUES (?, ?, ?, ?)", (ticker.upper(), qty, price, market_value))
                    cursor.execute("UPDATE port SET quantity = ?, price = ?,  market_value = ? WHERE ticker = ?", (new_cash_balance, 100, new_cash_balance, 'CASH'))
                    cursor.execute("INSERT INTO trans VALUES (?, ?, ?, ?, ?)", (date.today().strftime("%m/%d/%y"), ticker.upper(), qty, price, (qty * price)))

                # saves and closes out connection to db
                connection.commit()
                cursor.close()

            else:
                print('insufficient funds')

    def sell(self, ticker, qty):
        # establishes db connection
        connection = self.port
        cursor = connection.cursor()

        price = self.apisetup.quote(ticker.upper())['c']
        net_amount = price * qty
        ticker_balance = cursor.execute("SELECT quantity FROM port WHERE ticker = ?", (ticker.upper(),)).fetchone()[0]
        cash_bal = cursor.execute("SELECT quantity FROM port WHERE ticker = ?", ('CASH',)).fetchone()[0]

        try:
            if ticker_balance >= qty:
                new_balance = ticker_balance - qty
                new_market_value = new_balance * price
                new_cash_balance = cash_bal + net_amount
                if new_balance == 0:
                    cursor.execute("DELETE FROM port WHERE ticker = ?", (ticker.upper(),))
                    cursor.execute("UPDATE port SET quantity = ?, price = ?,  market_value = ? WHERE ticker = ?", (new_cash_balance, 100, new_cash_balance, 'CASH'))
                    cursor.execute("INSERT INTO trans VALUES (?, ?, ?, ?, ?)", (date.today().strftime("%m/%d/%y"), ticker.upper(), qty, price, net_amount))
                else:
                    cursor.execute("UPDATE port SET quantity = ?, price = ?,  market_value = ? WHERE ticker = ?", (new_balance, price, new_market_value, ticker.upper()))
                    cursor.execute("UPDATE port SET quantity = ?, price = ?,  market_value = ? WHERE ticker = ?", (new_cash_balance, 100, new_cash_balance, 'CASH'))
                    cursor.execute("INSERT INTO trans VALUES (?, ?, ?, ?, ?)", (date.today().strftime("%m/%d/%y"), ticker.upper(), qty, price, net_amount))
            else:
                print('insufficient balance')

            # saves and closes out connection to db
            connection.commit()
            cursor.close()

        except:
            print('No holdings of this security')

class SecurityInfo:
    def __init__(self, apisetup):
        self.apisetup = apisetup

    def currentprice(self, ticker):
        print(self.apisetup.quote(ticker.upper())['c'])

    def price_change(self, ticker):
        print(f"{ticker.upper()} price change: {self.apisetup.quote(ticker.upper())['d']}")

    def percent_change(self, ticker):
        print(f"{ticker.upper()} percent change: {self.apisetup.quote(ticker.upper())['dp']}")

    def high(self, ticker):
        print(f"{ticker.upper()} high of the day: {self.apisetup.quote(ticker.upper())['h']}")

    def low(self, ticker):
        print(f"{ticker.upper()} low of the day: {self.apisetup.quote(ticker.upper())['l']}")

    def open(self, ticker):
        print(f"{ticker.upper()} opening price: {self.apisetup.quote(ticker.upper())['o']}")

    def previous_close(self, ticker):
        print(f"{ticker.upper()} previous day close: {self.apisetup.quote(ticker.upper())['pc']}")

if __name__ == "__main__":
    # establishes db in class
    # as of right now you need ot run holdings and transactions method to create dbs before anything else is ran
    # will update this later

    # example:
    a = Portfolio(sqlite3.connect("Stock_Portfolio.db"), finnhub.Client(api_key=api_key))
    a.buy('msft', 3)
    a.transactions()
    a.holdings()







