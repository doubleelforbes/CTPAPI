# self dependencies
import pubcapi
import coin
import market
# Python dependencies
import datetime
import threading
import tkinter as tk
from tkinter import Label, LabelFrame, Entry, Text, Button, Listbox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter


# Functions
# Take a JSON list of coins and turn it into a dict of Coin objects.
def instantiatecoins(coindata):
    global coins
    # This is going to be the bigliest dict of coin objects ever.  I'm in there too!
    icoins = 0
    window.txtdebug.insert(tk.END, "Creating Coin Objects ...\r\n")
    for item in coindata:
        status = item.get("Status")
        name = item.get("Name")
        algorithm = item.get("Algorithm")
        maxwithdraw = item.get("MaxWithdraw")
        minwithdraw = item.get("MinWithdraw")
        symbol = item.get("Symbol")
        coinid = item.get("Id")
        depositconfirmations = item.get("DepositConfirmations")
        minbasetrade = item.get("MinBaseTrade")
        mintip = item.get("MinTip")
        tipenabled = item.get("IsTipEnabled")
        listingstatus = item.get("ListingStatus")
        withdrawfee = item.get("WithdrawFee")
        statusmsg = item.get("StatusMessage")
        # Instantiate a coin
        newcoinobj = coin.Coin(status, name, algorithm, maxwithdraw, minwithdraw, symbol, coinid,
                               depositconfirmations, minbasetrade, mintip, tipenabled, listingstatus, withdrawfee,
                               statusmsg)
        # Put it in a dict
        coins[symbol] = newcoinobj
        window.lstcoins.insert(tk.END, symbol)
        icoins = icoins + 1
    window.txtdebug.insert(tk.END, str(icoins) + " Coins Instantiated\r\n")
    window.txtdebug.see(tk.END)


# Take a JSON list of markets and turn it into a dict of Market objects.
def instantiatemarkets(marketdata):
    global coins
    global markets
    window.txtdebug.insert(tk.END, "Creating Market Objects ...\r\n")
    imarkets = 0
    ibasecurrencies = 0
    for item in marketdata:
        # json variables below
        status = item.get("Status")
        basesymbol = item.get("BaseSymbol")
        mintrade = item.get("MinimumTrade")
        maxtrade = item.get("MaximumTrade")
        maxprice = item.get("MaximumPrice")
        symbol = item.get("Symbol")
        maxbasetrade = item.get("MaximumBaseTrade")
        label = item.get("Label")
        currency = item.get("Currency")
        statusmsg = item.get("StatusMessage")
        tradefee = item.get("TradeFee")
        minprice = item.get("MinimumPrice")
        marketid = item.get("Id")
        basecurrency = item.get("BaseCurrency")
        minbasetrade = item.get("MinimumBaseTrade")
        # Instantiate a market
        newmarkobj = market.Market(status, basesymbol, mintrade, maxtrade, maxprice, symbol, maxbasetrade, label,
                                   currency, statusmsg, tradefee, minprice, marketid, basecurrency, minbasetrade, )
        markets[label] = newmarkobj
        imarkets = imarkets + 1
        # Mark the coin objects which represent base trading markets.
        if not coins[basesymbol].IsBaseCurrency:
            # Make it so!
            coins[basesymbol].IsBaseCurrency = True
            ibasecurrencies = ibasecurrencies + 1
            # Update GUI
            window.lstbasemarkets.insert(tk.END, coins[basesymbol].Symbol)
    # Let us know
    window.txtdebug.insert(tk.END, str(imarkets) + " Markets Instantiated\r\n" + str(ibasecurrencies) +
                           " New Base Currencies Identified.\r\n")
    window.txtdebug.see(tk.END)


# Coin list item select event.
def coinselect(event):
    global coins
    # Just dump the coin obj for now.
    if window.lstcoins.curselection():
        selectedcoin = window.lstcoins.get(window.lstcoins.curselection())
        window.txtdebug.insert(tk.END, coins[selectedcoin].tostring() + "\r\n")
        window.txtdebug.see(tk.END)


# Base market list select event.
def basemarketselect(event):
    global markets
    global graphdrawn
    # Clear the Trade Pair list
    tradepairsearchterm.set("")
    window.lsttradepairs.delete(0, tk.END)
    window.lstsellorders.delete(0, tk.END)
    window.lstbuyorders.delete(0, tk.END)
    window.lstmarkethistory.delete(0, tk.END)
    if graphdrawn:
        try:
            window.canvas.get_tk_widget().destroy()
        except:
            pass
        graphdrawn = False
    # BaseSymbol is the variable we want to check against our base market selection.
    if window.lstbasemarkets.curselection():
        selectedbasemarket = window.lstbasemarkets.get(window.lstbasemarkets.curselection())
        ibasemarkets = 0
        for key in markets:
            if markets[key].BaseSymbol == selectedbasemarket:
                window.lsttradepairs.insert(tk.END, markets[key].Label)
                ibasemarkets = ibasemarkets + 1
        window.txtdebug.insert(tk.END, selectedbasemarket + " Selected, " + str(ibasemarkets) + " markets listed.\r\n")
        window.txtdebug.see(tk.END)


# Keypress on search box event.
def tradepairsearch(keypress):
    global coins
    global markets
    global graphdrawn
    global tradepairsearchterm

    window.lsttradepairs.delete(0, tk.END)
    window.lstsellorders.delete(0, tk.END)
    window.lstbuyorders.delete(0, tk.END)
    window.lstmarkethistory.delete(0, tk.END)
    if graphdrawn:
        try:
            window.canvas.get_tk_widget().destroy()
        except:
            pass
        graphdrawn = False
    # That's the GUI cleared, on with the search!
    for key in markets:
        strkey = str(key)
        strsearch = tradepairsearchterm.get() + keypress.char
        basemarkets = window.lstbasemarkets.get(0, tk.END)
        if strsearch.upper() in basemarkets:
            strsearch = strsearch + "/"
        if strsearch.upper() in strkey:
            window.lsttradepairs.insert(tk.END, key)


# Trade pair list select event.
def tradepairselect(event):
    global graphdrawn
    global markets
    global lastmarketselect
    global orderreqthrds

    # Thread Function
    def tradepairfunc(threadpair):
        global markets
        global orderreqthrds
        # Request order data
        markets[threadpair].fillorders()
        markets[threadpair].fillmarkethistory()
        window.txtdebug.insert(tk.END, markets[threadpair].Label + " Data Received!\r\n")
        window.txtdebug.see(tk.END)
        # Recursion after thread completion, it's the only current way I can think to make sure a patient user is
        # awarded with a populated listed box.  Worst case scenario: The current selected market get's refreshed once
        # for every market request thread that completes.
        tradepairselect(event)
        # Self destroy the thread!
        del orderreqthrds[threadpair]

    # Clear the buy, sell and history lists & Graph
    window.lstbuyorders.delete(0, tk.END)
    window.lstsellorders.delete(0, tk.END)
    window.lstmarkethistory.delete(0, tk.END)
    if graphdrawn:
        try:
            window.canvas.get_tk_widget().destroy()
        except:
            pass
        graphdrawn = False
    # Dump the market tostring and grab the orders if we don't already have them
    if window.lsttradepairs.curselection():
        # Get this market selected
        selectedpair = window.lsttradepairs.get(window.lsttradepairs.curselection())
        # Do we already have this market data?
        if not markets[selectedpair].OrderDataFilled:
            # If we aren't already, ask for the information
            if selectedpair in orderreqthrds:
                if orderreqthrds[selectedpair].isAlive:
                    # The server may be in New Zealand methinks you're impatient!
                    window.txtdebug.insert(tk.END, "Still awaiting Data ...\r\n")
                    window.txtdebug.see(tk.END)
                else:
                    # OrderDataFilled is false, it must have expired.  Rerun the thread!
                    orderreqthrds[selectedpair].run()
            else:
                # Set up a new thread and put it in the list
                window.txtdebug.insert(tk.END, "Requesting " + selectedpair + " Order Data ...\r\n")
                window.txtdebug.see(tk.END)
                thrdorderdata = threading.Thread(target=tradepairfunc, args=(selectedpair,))
                orderreqthrds[selectedpair] = thrdorderdata
                orderreqthrds[selectedpair].start()
        else:
            # Populate the order boxes.
            # Copy both order lists and market history for the GUI
            lastmarketselect = selectedpair
            sellorders = markets[selectedpair].SellOrders
            buyorders = markets[selectedpair].BuyOrders
            markethistory = markets[selectedpair].MarketHistory
            for key in sorted(sellorders):
                window.lstsellorders.insert(tk.END, key)
            for key in sorted(buyorders, reverse=True):
                window.lstbuyorders.insert(tk.END, key)
            for key in markethistory:
                window.lstmarkethistory.insert(tk.END, key)
            window.txtdebug.insert(tk.END, markets[selectedpair].tostring() + "\r\n")
            window.txtdebug.see(tk.END)
            # The graph sometimes takes a we moment to draw if history is dense.  Not as long as an API call though.
            # So I'm going to try one uncontrolled graph thread on GUI populate.  There is a microfreeze on lsttradepair
            # Whilst waiting for matplotlib.
            graphthrd = threading.Thread(target=drawgraph, args=(markethistory,))
            graphthrd.start()

# Matplotlib graphing function using dict of market history objects.
def drawgraph(markethistory):
    global graphdrawn
    # Set up a graph and data sets
    timeplots = []
    priceplots = []
    # Set up the graph
    figgraph = Figure(figsize=(10, 10), dpi=60)
    # 2D Graph : 1 column, 1 Row, 1 Plot
    axes = figgraph.add_subplot(111)
    for key in markethistory:
        figgraph.suptitle(markethistory[key].Label)
        price = markethistory[key].Price
        timestamp = markethistory[key].Timestamp
        dtplot = datetime.datetime.fromtimestamp(timestamp)
        timeplots.insert(len(timeplots), dtplot)
        priceplots.insert(len(priceplots), price)
    # Enforce 8 decimal places
    axes.yaxis.set_major_formatter(FormatStrFormatter('%.8f'))
    # Plot the graph
    axes.plot(timeplots, priceplots)
    # Canvas placed in main frame, controlled by figgraph
    window.canvas = FigureCanvasTkAgg(figgraph, master=window.mainframe)
    window.canvas.get_tk_widget().place(relx=0.26, rely=0.01, relheight=0.46, relwidth=0.74)
    window.canvas.draw()
    graphdrawn = True


# Sell order list select event.
def sellorderselect(event):
    global lastmarketselect
    global markets
    # Just dump the sell orders for now
    if window.lstsellorders.curselection():
        selectedorder = window.lstsellorders.get(window.lstsellorders.curselection())
        sellorders = markets[lastmarketselect].SellOrders
        window.txtdebug.insert(tk.END, sellorders[selectedorder].tostring() + "\r\n")
        window.txtdebug.see(tk.END)


# Buy order list select event.
def buyorderselect(event):
    global lastmarketselect
    global markets
    # Just dump the buy orders for now
    if window.lstbuyorders.curselection():
        selectedorder = window.lstbuyorders.get(window.lstbuyorders.curselection())
        buyorders = markets[lastmarketselect].BuyOrders
        window.txtdebug.insert(tk.END, buyorders[selectedorder].tostring() + "\r\n")
        window.txtdebug.see(tk.END)


# Market history list select event.
def markethistoryselect(event):
    global lastmarketselect
    global markets
    # Just dump the historic trade for now
    if window.lstmarkethistory.curselection():
        selectedhistory = window.lstmarkethistory.get(window.lstmarkethistory.curselection())
        markethistory = markets[lastmarketselect].MarketHistory
        window.txtdebug.insert(tk.END, markethistory[selectedhistory].tostring() + "\r\n")
        window.txtdebug.see(tk.END)


# Refresh button event.
def refresh():
    global graphdrawn
    global thrdrefresh

    # Self threaded all singing all KNOWING refereshererupper
    # Clear the List boxes
    window.lstcoins.delete(0, tk.END)
    window.lstbasemarkets.delete(0, tk.END)
    window.lsttradepairs.delete(0, tk.END)
    window.lstsellorders.delete(0, tk.END)
    window.lstbuyorders.delete(0, tk.END)
    window.lstmarkethistory.delete(0, tk.END)
    if graphdrawn:
        try:
            window.canvas.get_tk_widget().destroy()
        except:
            pass
        graphdrawn = False

    def refreshfunc():
        # Grab BTC price & Instantiate Coins and Markets, We'll refresh the orders on market
        # select to keep it up to date.
        window.txtdebug.insert(tk.END, "Requesting current GBP to BTC price ...\r\n")
        window.txtdebug.see(tk.END)
        getbtcprice()
        window.txtdebug.insert(tk.END, "Requesting Cryptopia's currency list ...\r\n")
        window.txtdebug.see(tk.END)
        instantiatecoins(pcapi.getcurrencies())
        window.txtdebug.insert(tk.END, "Requesting Cryptopia's market list ...\r\n")
        window.txtdebug.see(tk.END)
        instantiatemarkets(pcapi.gettradepairs())

    thrdrefresh = threading.Thread(target=refreshfunc)
    thrdrefresh.setDaemon(True)
    thrdrefresh.start()


# Fetch current buy order for GBP > BTC
def getbtcprice():
    global btcgbp
    # The Api Class cheats a bit and uses blockcain.info to get the GBP price
    jsondata = pcapi.getbtcprice()
    # The api actually offers multiple currencies.  Enable the next line to see.
    # window.txtdebug.insert(tk.END, json.dumps(jsondata) + "\r\n")
    gbpdata = jsondata.get("GBP")
    btcgbp = gbpdata.get("buy")
    window.txtdebug.insert(tk.END, "BTC to GBP Price : " + gbpdata.get("symbol") + str(btcgbp) + "\r\n")
    window.txtdebug.see(tk.END)


# CLS on the textbox
def cleardebug():
    window.txtdebug.delete(1.0, tk.END)


# This is completely redundant since the window close calls this function instead of just destroying itself.
# Add code here to do stuff on exit.  Then when you realise it's a stupid idea, remove the code again.  But be sure
# to leave a single line which whispers to the interpreter window.destroy()
def on_closing():
    window.destroy()


# Assign matplotlib backend to TK
matplotlib.use("TkAgg")
# Create top level window object and variables
window = tk.Tk()
# A TK StringVar for holding search term
tradepairsearchterm = tk.StringVar()
# Instantiate an API object for use
pcapi = pubcapi.PubCApi()
# Empty lists to hold the coins and markets
coins = {}
markets = {}
lastmarketselect = ""
# The threads that bind us
thrdrefresh = threading.Thread
orderreqthrds = {}
graphdrawn = False
btcgbp = 0
# Base windows parameters
window.geometry("1024x768+450+150")
window.resizable(0, 0)
window.title("Cryptopia API")
window.iconbitmap("cryptopia.ico")
# A frame filled with some  buttons.  seems legit.
window.pubframe = LabelFrame(window, text="Public API Functions (No Key Required!)")
window.pubframe.place(relx=0.01, rely=0.01, relheight=0.07, relwidth=0.99)
# Refresh
window.btnrefresh = Button(window.pubframe, text="Refresh", command=refresh)
window.btnrefresh.place(relx=0.01, rely=0.01, height=24, width=65)
# Virtual gap, check x, y on buttons.
# Get BTC price.
window.btngetbtcprice = Button(window.pubframe, text="Get BTC Price", command=getbtcprice)
window.btngetbtcprice.place(relx=0.82, rely=0.01, height=24, width=85)
# Clear text output.
window.btncls = Button(window.pubframe, text="Clear Debug", command=cleardebug)
window.btncls.place(relx=0.91, rely=0.01, height=24, width=85)
# List boxes to hold coin and markets and their respective data
# a matplotlib graph will be thrown in here on getMarketHistory
window.mainframe = LabelFrame(window, text="Main")
window.mainframe.place(relx=0.01, rely=0.08, relheight=0.77, relwidth=0.99)
# Coins list
window.lblcoins = Label(window.mainframe, text="Coins")
window.lblcoins.place(relx=0.01, rely=0.01, relheight=0.03, relwidth=0.05)
window.lstcoins = Listbox(window.mainframe)
window.lstcoins.bind("<<ListboxSelect>>", coinselect)
window.lstcoins.place(relx=0.01, rely=0.04, relheight=0.94, relwidth=0.05)
# Base Market List
window.lblbasemarkets = Label(window.mainframe, text="Base Coins")
window.lblbasemarkets.place(relx=0.06, rely=0.01, relheight=0.03, relwidth=0.08)
window.lstbasemarkets = Listbox(window.mainframe, exportselection=False)
window.lstbasemarkets.bind("<<ListboxSelect>>", basemarketselect)
window.lstbasemarkets.place(relx=0.06, rely=0.04, relheight=0.18, relwidth=0.08)
# Search Trade Pairs
window.lblsearchpairs = Label(window.mainframe, text="Search Pairs")
window.lblsearchpairs.place(relx=0.06, rely=0.22, relheight=0.03, relwidth=0.08)
window.txtsearchpairs = Entry(window.mainframe, textvariable=tradepairsearchterm)
window.txtsearchpairs.bind("<Key>", tradepairsearch)
window.txtsearchpairs.place(relx=0.06, rely=0.25, relheight=0.03, relwidth=0.08)
# Trade Pair Sub-List (Either by Base Market Select or Search)
window.lbltradepairs = Label(window.mainframe, text="Trade Pairs")
window.lbltradepairs.place(relx=0.06, rely=0.29, relheight=0.03, relwidth=0.08)
window.lsttradepairs = Listbox(window.mainframe, exportselection=False)
window.lsttradepairs.bind("<<ListboxSelect>>", tradepairselect)
window.lsttradepairs.place(relx=0.06, rely=0.32, relheight=0.66, relwidth=0.08)
# Sell orders
window.lblsellorders = Label(window.mainframe, text="Sell Orders")
window.lblsellorders.place(relx=0.14, rely=0.01, relheight=0.03, relwidth=0.12)
window.lstsellorders = Listbox(window.mainframe)
window.lstsellorders.bind("<<ListboxSelect>>", sellorderselect)
window.lstsellorders.place(relx=0.14, rely=0.04, relheight=0.45, relwidth=0.12)
# Buy Orders
window.lblbuyorders = Label(window.mainframe, text="Buy Orders")
window.lblbuyorders.place(relx=0.14, rely=0.49, relheight=0.03, relwidth=0.12)
window.lstbuyorders = Listbox(window.mainframe)
window.lstbuyorders.bind("<<ListboxSelect>>", buyorderselect)
window.lstbuyorders.place(relx=0.14, rely=0.53, relheight=0.45, relwidth=0.12)
# Market History
window.lblmarkethistory = Label(window.mainframe, text="Market History")
window.lblmarkethistory.place(relx=0.26, rely=0.47, relheight=0.03, relwidth=0.74)
window.lstmarkethistory = Listbox(window.mainframe)
window.lstmarkethistory.bind("<<ListboxSelect>>", markethistoryselect)
window.lstmarkethistory.place(relx=0.26, rely=0.50, relheight=0.48, relwidth=0.74)
# A Debug frame with a textbox.  seems legit.
window.debugframe = LabelFrame(window, text="Debug")
window.debugframe.place(relx=0.01, rely=0.85, relheight=0.15, relwidth=0.99)
window.txtdebug = Text(window.debugframe)
window.txtdebug.place(relx=0.01, rely=0.01, relheight=0.96, relwidth=0.98)
# Start the gui loop but run a function before quitting.
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
