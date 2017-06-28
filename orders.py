# Data storage class for live order information
class Order:
    def __init__(self, key, otype, tradepairid, label, price, volume, total):
        self.Key = key
        self.Type = otype
        self.TradePairID = tradepairid
        self.Label = label
        self.Price = price
        self.Volume = volume
        self.Total = total

    def tostring(self):
        # Volume, Total and Price are raw numbers.  We will have to format them as a standard crypto price.
        formattedvolume = "{0:.8f}".format(self.Volume)
        formattedtotal = "{0:.8f}".format(self.Total)
        formattedprice = "{0:.8f}".format(self.Price)
        return ("|" + self.Label + "| " + self.Type + " " + formattedvolume + " @ " + formattedprice
                + " | Total: " + formattedtotal + " |")
