# Data Container class for holding coin information.
class Coin:
    def __init__(self, status, name, algorithm, maxwithdraw, minwithdraw, symbol, coinid, depositconfirmations,
                 minbasetrade, mintip, tipenabled, listingstatus, withdrawfee, statusmsg):
        self.Status = status
        self.Name = name
        self.Algorithm = algorithm
        self.MaxWithdraw = maxwithdraw
        self.MinWithdraw = minwithdraw
        self.Symbol = symbol
        self.CoinId = coinid
        self.DepositConfirmations = depositconfirmations
        self.MinBaseTrade = minbasetrade
        self.MinTip = mintip
        self.IsTipEnabled = tipenabled
        self.ListingStatus = listingstatus
        self.WithdrawFree = withdrawfee
        self.StatusMessage = str(statusmsg)
        self.IsBaseCurrency = False

    def tostring(self):
        return ("| Name : (" + self.Symbol + ") " + self.Name + " | Algorithm : " + self.Algorithm + " | Status : "
                + self.Status + " | Message :" + self.StatusMessage + " |")
