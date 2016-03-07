oandapy
======
oandapy is a python wrapper for OANDA's REST API.

Install
======

Using pip:

    $ pip install git+https://github.com/oanda/oandapy.git

oandapy depends on python-requests, which will be installed automatically.

Usage
======

Include the oandapy module and create an oandapy instance with your account credentials. For FxGame and FxTrade, an access token must be provided.

	import oandapy

	oanda = oandapy.API(environment="practice", access_token="abcdefghijk...")

Keyword arguments to functions are mapped to the functions available for each endpoint in the [Oanda API docs](http://developer.oanda.com/), so changes to the API aren't held up from you using them by this library. For each api call, oandapy returns a native python object, converted from JSON so you don't have to.

The EndpointsMixin class in [oandapy.py](oandapy/oandapy.py) holds a mixin of all Oanda API endpoints.

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
Since these methods are abstract methods, you need to override these methods
to handle the streaming data.

The following example prints _count_ ticks from the stream then disconnects.


    class MyStreamer(oandapy.Streamer):
        def __init__(self, count=10, *args, **kwargs):
            super(MyStreamer, self).__init__(*args, **kwargs)
            self.count = count
            self.reccnt = 0

        def on_success(self, data):
            print data, "\n"
            self.reccnt += 1
            if self.reccnt == self.count:
                self.disconnect()

        def on_error(self, data):
            self.disconnect()


Initialize an instance of your custom streamer, and start connecting to the stream.
See http://developer.oanda.com/rest-live/streaming/ for further documentation.

    account = "12345"
    stream = MyStreamer(environment="practice", access_token="abcdefghijk...")
    stream.rates(account, instruments="EUR_USD,EUR_JPY,US30_USD,DE30_EUR")


The same procedure can be used for streaming events.


    stream = MyStreamer(environment="practice", access_token="abcdefghijk...")
    stream.events(ignore_heartbeat=False)

