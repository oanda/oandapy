import unittest
import oandapy
import sys
from . import unittestsetup
from .unittestsetup import environment as environment

try:
    from nose_parameterized import parameterized, param
except:
    print("*** Please install 'nose_parameterized' to run these tests ***")
    exit(0)

access_token = None
account = None
api = None

instruments = ["EUR_USD", "EUR_JPY", "US30_USD", "DE30_EUR"]


class DisconnectException(Exception):
    pass


class Stream(oandapy.Streamer):
    """
        class to parse the OANDA stream
        tick records are processed into candles of different timeframes
        candles that are ready are processed by the plugin manager
    """
    def __init__(self, count=10, *args, **kwargs):
        super(Stream, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0
        self.hbcnt = 0

    def on_success(self, data):
        print(data)
        if "heartbeat" in data:
            self.hbcnt += 1
        else:
            self.reccnt += 1

        if self.reccnt + self.hbcnt == self.count:
            self.disconnect()

    def on_error(self, data):
        self.disconnect()


class TestRates(unittest.TestCase):

    def setUp(self):
        global access_token
        global account
        global api

        try:
            account, access_token = unittestsetup.auth()
        except Exception as e:
            print("%s" % e)
            exit(0)

        api = oandapy.API(environment=environment, access_token=access_token)

    @parameterized.expand([(25, False),
                           (25, True)])
    def test_Rates(self, count, ignore_heartbeat=False):
        """ get records from stream """
        # recs received should equal #recs requested + # hb recs
        instruments = ["EUR_USD", "US30_USD", "DE30_EUR"]
        r = Stream(access_token=access_token, environment=environment,
                   count=count)
        r.rates(account, ignore_heartbeat=ignore_heartbeat,
                instruments=",".join(instruments))

        if ignore_heartbeat:
            self.assertEqual(count, r.reccnt)
        else:
            self.assertEqual(count, r.reccnt + r.hbcnt)

    @parameterized.expand([(4, False),
                           ])
    def test__Events(self, count, ignore_heartbeat=False):
        """ get account events from stream """
        # if ignoring heartbeats this test will keep waiting
        # this could be solved by creating trades in parallel that
        # generate events
        # heartbeats are every 15 sec.
        r = Stream(access_token=access_token,
                   environment=environment, count=count)
        r.events(ignore_heartbeat=False)
        self.assertEqual(count, r.reccnt + r.hbcnt)


if __name__ == "__main__":

    unittest.main()
