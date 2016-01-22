import json
import requests
from abc import ABCMeta, abstractmethod

""" OANDA API wrapper for OANDA's REST API """

""" HTTPS Streaming """


class Streamer(object):
    """ Provides functionality for HTTPS Streaming
    Docs: http://developer.oanda.com/rest-live/streaming
    """
    __metaclass__ = ABCMeta

    def __init__(self, environment="practice", access_token=None):
        """Instantiates an instance of OandaPy's streaming API wrapper.
        :param environment: (optional) Provide the environment for oanda's
         REST api, either 'practice', or 'live'. Default: practice
        :param access_token: (optional) Provide a valid access token if you
         have one. This is required if the environment is not sandbox.
        """

        if environment == 'practice':
            self.api_url = 'https://stream-fxpractice.oanda.com/v1/prices'
        elif environment == 'live':
            self.api_url = 'https://stream-fxtrade.oanda.com/v1/prices'

        self.access_token = access_token
        self.client = requests.Session()
        self.client.stream = True
        self.connected = False

        # personal token authentication
        if self.access_token:
            self.client.headers['Authorization'] = 'Bearer '+self.access_token

    def start(self, ignore_heartbeat=True, **params):
        """ Starts the stream with the given parameters
        :param accountId: (Required) The account that prices are applicable for
        :param instruments: (Required) A (URL encoded) comma separated list of
         instruments to fetch prices for.
        :param ignore_heartbeat: (optional) Whether or not to display the
         heartbeat. Default: True
        """
        self.connected = True

        request_args = {}
        request_args['params'] = params

        while self.connected:
            response = self.client.get(self.api_url, **request_args)

            if response.status_code != 200:
                self.on_error(response.content)

            for line in response.iter_lines(90):
                if not self.connected:
                    break

                if line:
                    data = json.loads(line.decode("utf-8"))
                    if not (ignore_heartbeat and "heartbeat" in data):
                        self.on_success(data)

    @abstractmethod
    def on_success(self, data):
        """ Called when data is successfully retrieved from the stream
        Override this to handle your streaming data.
        :param data: response object sent from stream
        """

        return True

    @abstractmethod
    def on_error(self, data):
        """ Called when stream returns non-200 status code
        Override this to handle your streaming data.
        :param data: error response object sent from stream
        """

        return

    def disconnect(self):
        """ Manually disconnects the streaming client
        """
        self.connected = False
