# Data storage class for market order history
import datetime


class MarketHistory:
    def __init__(self, tradepairid, label, otype, price, amount, total, timestamp):
        self.TradePairID = tradepairid
        self.Label = label
        self.Type = otype
        self.Price = price
        self.Amount = amount
        self.Total = total
        self.Timestamp = timestamp

    def tostring(self):
        strprice = "{0:.8f}".format(self.Price)
        stramount = "{0:.8f}".format(self.Amount)
        strtotal = "{0:.8f}".format(self.Total)
        datetimestamp = str(datetime.datetime.fromtimestamp(self.Timestamp))
        return("|" + self.Label + "| " + self.Type + " " + stramount + " @ " + strprice + " Total: "
               + strtotal + " |TIME : " + datetimestamp + "|")
