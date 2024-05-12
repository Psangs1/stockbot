from stockcommands.stock import *

MAX_STOCKS = 5
class myPortfolio:
    def __init__(self):
        self.portfolio = {}
        self.stockprice = {}
        self.totalreturns = 0

    def currentStockPrices(self):
        for stock in self.portfolio:
            self.stockprice.update({stock : float(get_stock_price(stock))})
        
    def addStock(self, stock, quantity):
        if len(self.portfolio) >= MAX_STOCKS:
            return False, "You already have the maximum number of stocks in your portfolio."
        if stock_exists(stock) == False:
            return False, "Stock does not exist."
        #figure out total stock price
        print(type(get_stock_price(stock)))
        totalprice = float(quantity) * (get_stock_price(stock))
        self.portfolio.update({stock : totalprice})
        self.portfolio[stock] += totalprice
        return True, f"Added {quantity} shares of {stock} to your portfolio."

    def removeStock(self, stock, quantity):
        quantity = float(quantity)
        if(stock not in self.portfolio):
            return False, f"{stock} is not in your portfolio."
        self.portfolio[stock] -= quantity
        if self.portfolio[stock] <= 0:
            del self.portfolio[stock]

    def trackPortfolio(self):
        netreturns = 0
        netreturnpersymbol = []
        for symbol, totalprice in self.portfolio.items():
            currentprice = float(get_stock_price(symbol)) * self.getQuantity(symbol)
            netreturns += (currentprice - totalprice)
            netreturnpersymbol.append(currentprice - totalprice)
        return netreturns, netreturnpersymbol
    def getQuantity(self, stock):
        return self.portfolio.get(stock) / float(get_stock_price(stock))
    
    def getStocks(self):
        return self.portfolio.keys()
        