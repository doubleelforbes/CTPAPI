# Public API Class for cryptopia.co.nz
# Python Dependencies
import json
import urllib.request


class PubCApi:
    def __init__(self):
        # Nothing to see here just a gangly class with self contained limbs ;)
        pass

    def getbtcprice(self):
        # Using blockchain url : https://blockchain.info/ticker
        # I know I know! But Cryptopia doesn't offer currency rates
        # It's just a raw json return
        requrl = "https://blockchain.info/ticker"
        response = urllib.request.urlopen(requrl).read()
        jsondata = response.decode('utf-8')
        data = json.loads(jsondata)
        return data

    def getcurrencies(self):
        # GET https://www.cryptopia.co.nz/api/GetCurrencies
        # await response and return object for instantiation
        return self.makejsonquery("GetCurrencies")

    def gettradepairs(self):
        # GET https://www.cryptopia.co.nz/api/GetTradePairs
        # await response and return object for instantiation
        return self.makejsonquery("GetTradePairs")

    def getmarkets(self, basecurr="BTC", hours="12"):
        # GET https://www.cryptopia.co.nz/api/GetMarkets
        # Param: baseMarket (optional, default: All)
        # Param: hours (optional, default: 24)
        # GET https://www.cryptopia.co.nz/api/GetMarkets/BTC
        # GET https://www.cryptopia.co.nz/api/GetMarkets/12
        # GET https://www.cryptopia.co.nz/api/GetMarkets/BTC/12
        # await response and return object for instantiation
        return self.makejsonquery("GetMarkets/" + basecurr + "/" + hours)

    def getmarket(self, market="DOT_BTC", hours="24"):
        # Param: market (Required) (TradePairId or MarketName)
        # GET https://www.cryptopia.co.nz/api/GetMarket/100
        # GET https://www.cryptopia.co.nz/api/GetMarket/DOT_BTC
        # Param: hours(optional, default: 24)
        # GET https://www.cryptopia.co.nz/api/GetMarket/100/6
        # await response and return object for instantiation
        return self.makejsonquery("GetMarket/" + market + "/" + hours)

    def getmarkethistory(self, tradepair="DOT_BTC", hours="24"):
        # Param: market (Required) (TradePairId or MarketName)
        # GET https://www.cryptopia.co.nz/api/GetMarketHistory/100
        # GET https://www.cryptopia.co.nz/api/GetMarketHistory/DOT_BTC
        # Param: hours (optional, default: 24)
        # GET https://www.cryptopia.co.nz/api/GetMarketHistory/100/48
        # GET https://www.cryptopia.co.nz/api/GetMarketHistory/DOT_BTC/48
        return self.makejsonquery("GetMarketHistory/" + tradepair + "/" + hours)

    def getmarketorders(self, tradepair="DOT_BTC", count="100"):
        # Param: market (Required) (TradePairId or MarketName)
        # GET https://www.cryptopia.co.nz/api/GetMarketOrders/100
        # GET https://www.cryptopia.co.nz/api/GetMarketOrders/DOT_BTC
        # Param: orderCount (optional, default: 100)
        # GET https://www.cryptopia.co.nz/api/GetMarketOrders/100/50
        # GET https://www.cryptopia.co.nz/api/GetMarketOrders/DOT_BTC/50
        # await response and return object for instantiation
        return self.makejsonquery("GetMarketOrders/" + tradepair + "/" + count)

    def getmarketordergroups(self, marketlist="DOT_BTC-DOT_LTC-DOT_DOGE-DOT_UNO", count="100"):
        # Param: markets(Required)(TradePairIds or MarketNames separated by '-')
        # GET https://www.cryptopia.co.nz/api/GetMarketOrderGroups/100-101-102-103
        # GET https://www.cryptopia.co.nz/api/GetMarketOrderGroups/DOT_BTC-DOT_LTC-DOT_DOGE-DOT_UNO
        # Param: orderCount(optional, default: 100)
        # GET https://www.cryptopia.co.nz/api/GetMarketOrderGroups/100-101-102-103/50
        # GET https://www.cryptopia.co.nz/api/GetMarketOrderGroups/DOT_BTC-DOT_LTC-DOT_DOGE-DOT_UNO/50
        return self.makejsonquery("GetMarketOrderGroups/" + marketlist + "/" + count)

    def makejsonquery(self, funcandparamurl):
        # HTTP GET to URL "https://www.cryptopia.co.nz/api/" + funcandparamurl return json object
        # HTTP Subdirectories are commented for each function above, I'm just cutting redundancy, sheesh!
        requrl = "https://www.cryptopia.co.nz/api/" + funcandparamurl
        response = urllib.request.urlopen(requrl).read()
        jsondata = response.decode('utf-8')
        data = json.loads(jsondata)
        # Either return the data list or return the error msg.  The API offers a success field but this is still True
        # in the event of an error returned.
        if not data.get("Error"):
            return data.get("Data")
        else:
            return data.get("Error")
