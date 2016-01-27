""" initialization of unittests and data for unittests """

import time
environment = "practice"

# calculate expiryDate as an offset from today
# now + 5 days
days = 5
expiryDate = time.strftime("%Y-%m-%dT%H:%M:%S",
                           time.localtime(int(time.time() + 86400*days)))

# Some order specs. used in various tests
orders = {
    # market order
    "EUR_GBP_market": {
        "instrument": "EUR_GBP",
        "units": 1000,
        "side": "buy",
        "type": "market"
    },
    # market order
    "EUR_JPY_market": {
        "instrument": "EUR_JPY",
        "units": 1000,
        "side": "buy",
        "type": "market"
    },
    # market order
    "EUR_USD_market": {
        "instrument": "EUR_USD",
        "units": 1000,
        "side": "buy",
        "type": "market"
    },
    # limit order
    "EUR_USD_limit": {
        "instrument": "EUR_USD",
        "units": 1000,
        "side": "buy",
        "price": "0.7",
        "type": "limit",
        "expiry": expiryDate,
    },
    # limit order: deliberately missing expiry
    "EUR_USD_limit_No_expiry": {
        "instrument": "EUR_USD",
        "units": 1000,
        "side": "buy",
        "price": "0.7",
        "type": "limit",
    },
}


def auth():
    access_token = None
    account = None
    with open("tests/account.txt") as T:
        account = T.read().strip()
    with open("tests/token.txt") as T:
        access_token = T.read().strip()

    if account == "9999999":
        raise Exception(
              "\n"
              "***************************************************\n"
              "*** PLEASE PROVIDE YOUR account AND token IN   ****\n"
              "*** account.txt AND token.txt TO RUN THE TESTS ****\n"
              "***************************************************\n")

    return account, access_token
