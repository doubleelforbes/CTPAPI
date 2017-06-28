# CTPAPI
Cryptopia Public API Frontend

Cryptopia.co.nz offers both Public and Private API's for accessing their market data.
CTPAPA (Cryptopia Public API) offers a desktop based interface to the live market info,
as well as 7 day market history.

The Code
========
Coin, Market, Order and MarketHistory Classes are designed to store units of data from the JSON
object returned from the API.  The last two are stored in lists within each Market object which
is stored in a list within main.py, as are Coins.
Most should find it well commented enough to understand.
This is my first attempt at anything in Python, the project began under a 2.7 install then was corrected
after a 3.6 update.

The GUI
=======
A Simple refresh button to update coin and market data.
A Get BTC price button (GBP, easy to change in code)
A Clear Debug
All listboxes will invoke a ToString() for the object it represents.
In the case of a Trade Pair select: buy, sell and market history data is pulled from the API.
This data self expires within the Market class after 5 minutes.
There is a delay on graph drawing in the case of dense market history.
This leaves a bug where, if overwhelmed, the threads can leave a second canvase on the GUI which is never destroyed.
The program resumes normal operation.
