oandapy
======
oandapy is a python wrapper for OANDA's REST API.

Install
======

python-requests is required. Using pip:

    $ pip install requests

Usage
======

Include the oandapy module and create an oandapy instance with your account credentials. For FxGame and FxTrade, an access token must be provided.

	import oandapy

	oanda = oandapy.API(environment="practice", access_token="abcdefghijk...")

Keyword arguments to functions are mapped to the functions available for each endpoint in the [Oanda API docs](http://developer.oanda.com/docs/), so changes to the API aren't held up from you using them by this library. For each api call, oandapy returns a native python object, converted from JSON so you don't have to.

The EndpointsMixin class in [oandapy.py](oandapy.py) holds a mixin of all Oanda API endpoints.

Examples
======

### Get price for an instrument
	response = oanda.get_prices(instruments="EUR_USD")
	prices = response.get("prices")
	asking_price = prices[0].get("ask")

### Open a limit order
	# required datetime functions
	from datetime import datetime, timedelta

	# sample account_id
	account_id = 1813880

	# set the trade to expire after one day
	trade_expire = datetime.utcnow() + timedelta(days=1)
	trade_expire = trade_expire.isoformat("T") + "Z"

	response = oanda.create_order(account_id, 
	    instrument="USD_CAD",
	    units=1000,
	    side='sell',
	    type='limit',
	    price=1.15,
	    expiry=trade_expire
	)

Rates Streaming
======
Create a custom streamer class to setup how you want to handle the data. 
Each tick is sent through the `on_success` and `on_error` functions.
You can override these functions to handle the streaming data.

The following example prints the first 10 ticks from the stream then disconnects.

    class MyStreamer(oandapy.Streamer):
        def __init__(self, *args, **kwargs):
            oandapy.Streamer.__init__(self, *args, **kwargs)
            self.ticks = 0

        def on_success(self, data):
            self.ticks += 1
            print data
            if self.ticks == 10:
                self.disconnect()

        def on_error(self, data):
            self.disconnect()

Initialize an instance of your custom streamer, and start connecting to the stream.
See http://developer.oanda.com/docs/v1/stream/#rates-streaming for further documentation.

    stream = MyStreamer(environment="practice", access_token="abcdefghijk...")
    stream.start(accountId=12345, instruments="EUR_USD,USD_CAD")
