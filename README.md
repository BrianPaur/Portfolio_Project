# Portfolio Tracker

Creates a stock portfolio for the user and has the ability to pull in various security datapoints (finnhub API).
- On first run return transaction and holdings function to create dbs (will update latrer so that we don't have to do this)

Portfolio Functions (all transaction funcs will update transaction db)
- holdings (displays portfolio and calls current price everytime function is ran)
- transactions (displays all transactions with time stamp)
- deposit cash
- withdraw cash
- buy
- sell
- buying power (how much of a stock you can afford)

![image](https://user-images.githubusercontent.com/48654156/172747961-da35349c-9c5f-4cd7-a9e8-ec86ba7ec869.png)

Security Info Functions
- current price
- percent change
- high
- low
- open
- previous close

![image](https://user-images.githubusercontent.com/48654156/172748156-e8058913-bfa1-4cde-bd5f-5702fedc3048.png)

![image](https://user-images.githubusercontent.com/48654156/172748171-4a1fc6bc-f046-49af-b153-5709bf291ec6.png)

To-Do
- add totals to pd table for holdings
- host on flask app


