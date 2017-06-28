# Market storage class which holds data for each trade pair, as well as buy and sell order object lists.
# And a market history object list.
# Python Dependencies
from threading import Timer
# Self Dependencies
import pubcapi
import orders
import markethistory
pcapi = pubcapi.PubCApi()


class Market:
    def __init__(self, status, basesymbol, mintrade, maxtrade, maxprice, symbol, maxbasetrade, label, currency,
                 statusmsg, tradefee, minprice, marketid, basecurrency, minbasetrade,):
        self.Status = status
        self.BaseSymbol = basesymbol
        self.MinimumTrade = mintrade
        self.MaximumTrade = maxtrade
        self.MaximumPrice = maxprice
        self.Symbol = symbol
        self.MaximumBaseTrade = maxbasetrade
        self.Label = label
        self.Currency = currency
        self.StatusMessage = statusmsg
        self.TradeFee = tradefee
        self.MinimumPrice = minprice
        self.MarketID = marketid
        self.BaseCurrency = basecurrency
        self.MinimumBaseTrade = minbasetrade
        self.SellOrders = {}
        self.BuyOrders = {}
        self.MarketHistory = {}
        self.OrderDataFilled = False

    def tostring(self):
        return ("| Market: " + self.Label + " | Status : " + self.Status + " | Message: " + str(self.StatusMessage)
                + " |")

    # Fill own buy and sell order lists
    def fillorders(self):
        # We're going to create a new order object for each live order, storing them in two dicts for Sell and Buy
        # The Data key holds two more dicts, Buy and Sell
        ordersdata = pcapi.getmarketorders(str(self.MarketID), "100")
        buyorders = ordersdata.get("Buy")
        sellorders = ordersdata.get("Sell")
        # Iterate and Instantiate both data sets
        # Identical routines, differing dicts
        for buyitem in buyorders:
            tradepairid = buyitem.get("TradePairID")
            label = buyitem.get("Label")
            price = buyitem.get("Price")
            volume = buyitem.get("Volume")
            total = buyitem.get("Total")
            key = "{0:0>19.8f}".format(price)
            otype = "BUY"
            newbuyobj = orders.Order(key, otype, tradepairid, label, price, volume, total)
            self.BuyOrders[key] = newbuyobj
        for sellitem in sellorders:
            tradepairid = sellitem.get("TradePairID")
            label = sellitem.get("Label")
            price = sellitem.get("Price")
            volume = sellitem.get("Volume")
            total = sellitem.get("Total")
            key = "{0:0>19.8f}".format(price)
            otype = "SELL"
            newsellobj = orders.Order(key, otype, tradepairid, label, price, volume, total)
            self.SellOrders[key] = newsellobj

    # Fill own market history list.
    def fillmarkethistory(self):
        historydata = pcapi.getmarkethistory(str(self.MarketID), "168")
        for historyitem in historydata:
            tradepairid = historyitem.get("TradePairID")
            label = historyitem.get("Label")
            otype = historyitem.get("Type")
            price = historyitem.get("Price")
            amount = historyitem.get("Amount")
            total = historyitem.get("Total")
            timestamp = historyitem.get("Timestamp")
            newhistoryobj = markethistory.MarketHistory(tradepairid, label, otype, price, amount, total, timestamp)
            key = newhistoryobj.tostring()
            self.MarketHistory[key] = newhistoryobj
        # Mark the market as orders instantiated.
        self.OrderDataFilled = True
        # Start a timer and we'll mark the order data out of date.
        orderexpiry = Timer(300.0, self.expiredata)
        orderexpiry.start()
        # Make a further call to the API for 24 hour stats on this market
        recentmarketdata = pcapi.getmarket(str(self.MarketID), "24")
        self.AskPrice = recentmarketdata.get("AskPrice")
        self.BidPrice = recentmarketdata.get("BidPrice")
        self.Low = recentmarketdata.get("Low")
        self.High = recentmarketdata.get("High")
        self.Volume = recentmarketdata.get("Volume")
        self.Change = recentmarketdata.get("Change")
        self.Open = recentmarketdata.get("Open")
        self.Close = recentmarketdata.get("Close")
        self.BaseVolume = recentmarketdata.get("BaseVolume")
        self.BaseBuyVolume = recentmarketdata.get("BaseBuyVolume")
        self.BaseSellVolume = recentmarketdata.get("BaseSellVolume")

    # On creation a five minute timer is created to destroy the data so that we know to request it again.
    # There is scope to just call the self order fillers, however with 1600 markets that may not be wise.
    def expiredata(self):
        # Clear the order data.
        self.OrderDataFilled = False
        self.SellOrders = {}
        self.BuyOrders = {}
        self.MarketHistory = {}

