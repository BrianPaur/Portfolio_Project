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

Security Info Functions
- current price
- percent change
- high
- low
- open
- previous close

To-Do
- add totals to pd table for holdings
- host on flask app
