import unittest
import oandapy
import sys
from . import unittestsetup
from .unittestsetup import environment as environment

access_token = None
account = None
api = None

instruments = ["EUR_USD", "EUR_JPY", "US30_USD", "DE30_EUR"]


class DisconnectException(Exception):
    pass


class MyStream(oandapy.Streamer):

    def __init__(self, count=10, *args, **kwargs):
        super(MyStream, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0

    def on_success(self, data):
        print data, "\n"
        self.reccnt += 1
        if self.reccnt == self.count:
            self.disconnect()

    def on_error(self, data):
        self.disconnect()
        # raise DisconnectException()


class TestRates(unittest.TestCase):

    def setUp(self):
        global access_token
        global account

        try:
            account, access_token = unittestsetup.auth()
        except Exception as e:
            print("%s" % e)
            exit(0)

    def test__Rates(self):
        count = 10
        r = MyStream(access_token=access_token,
                     environment=environment, count=count)
        r.rates(account, instruments=",".join(instruments))
        self.assertEqual(count, r.reccnt)

    def test__Events(self):
        count = 4
        r = MyStream(access_token=access_token,
                     environment=environment, count=count)
        r.events(ignore_heartbeat=False)
        self.assertEqual(count, r.reccnt)


if __name__ == "__main__":

    unittest.main()
