import unittest
import oandapy
import sys

access_token = None
account = None


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

    # in case we want heartbeats by default: override start()
    # def start(self, ignore_heartbeat=False, **params):
    #     super(Stream, self).start(ignore_heartbeat=ignore_heartbeat, **params)

    def on_success(self, data):
        print data, "\n"
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
        with open("tests/token.txt") as T:
                access_token = T.read().strip()
        with open("tests/account.txt") as T:
                account = T.read().strip()
        if account == "9999999":
            warning = """
             ***************************************************
             *** PLEASE PROVIDE YOUR account AND token IN   ****
             *** account.txt AND token.txt TO RUN THE TESTS ****
             ***************************************************
             """
            print warning

    def test_Rates(self):
        """ get records from stream and including heartbeats,
            #recs received should equal #recs requested + # hb recs
        """
        count = 100
        count = 10
        instruments = ["EUR_USD", "US30_USD", "DE30_EUR"]
        r = Stream(access_token=access_token, environment="practice",
                   count=count)
        r.start(accountId=account, ignore_heartbeat=False,
                instruments=",".join(instruments))
        self.assertEqual(count, r.reccnt + r.hbcnt)

    def test_RatesNoHeartBeats(self):
        """ get records from stream and ignore heartbeats,
            #recs received should equal #recs requested
        """
        count = 100
        instruments = ["EUR_USD", "US30_USD", "DE30_EUR"]
        r = Stream(access_token=access_token, environment="practice",
                   count=count)
        r.start(accountId=account, ignore_heartbeat=True,
                instruments=",".join(instruments))

        self.assertEqual(count, r.reccnt)


if __name__ == "__main__":

    unittest.main()
