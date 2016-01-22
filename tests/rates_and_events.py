import unittest
import oandapy
import sys

access_token = None
account = None


class DisconnectException(Exception):
    pass


class MyStream(oandapy.Streamer):
    """
        class to parse the OANDA stream
        tick records are processed into candles of different timeframes
        candles that are ready are processed by the plugin manager
    """
    def __init__(self, count=10, *args, **kwargs):
        super(MyStream, self).__init__(*args, **kwargs)
        self.count = count
        self.reccnt = 0

    def run(self, endpoint, ignore_heartbeat=False, **params):
        # We want the heartbeats
        super(MyStream, self).run(endpoint, ignore_heartbeat, **params)

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
        with open("tests/token.txt") as T:
                access_token = T.read().strip()
        with open("tests/account.txt") as T:
                account = T.read().strip()

        if account == "9999999":
            print("\n***************************************************\n"
                    "*** PLEASE PROVIDE YOUR account AND token IN   ****\n"
                    "*** account.txt AND token.txt TO RUN THE TESTS ****\n"
                    "***************************************************\n")

    def test_Rates(self):
        count = 10
        r = MyStream(access_token=access_token,
                     environment="practice", count=count)
        r.rates(account, instruments="EUR_USD,EUR_JPY,US30_USD,DE30_EUR")
        self.assertEqual(count, r.reccnt)

    def test_Events(self):
        count = 4
        r = MyStream(access_token=access_token,
                     environment="practice", count=count)
        r.events(ignore_heartbeat=False)
        self.assertEqual(count, r.reccnt)


if __name__ == "__main__":

    unittest.main()
