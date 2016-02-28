import warnings

import json
import requests
from exceptions import BadEnvironment
from abc import ABCMeta, abstractmethod

""" OANDA API wrapper for OANDA's REST API """

""" HTTPS Streaming """


class EndpointsMixin(object):

    """Stream"""

    def rates(self, account_id, instruments, **params):
        """ Get streaming rates
        Docs: http://developer.oanda.com/rest-live/streaming
        :param accountId: (Required) The account that prices are applicable for
        :param instruments: (Required) A (URL encoded) comma separated list of
         instruments to fetch prices for.
        """
        params['accountId'] = account_id
        params['instruments'] = instruments
        endpoint = 'v1/prices'
        return self.run(endpoint, params=params)

    def events(self, **params):
        """ Get streaming events
        Docs: http://developer.oanda.com/rest-live/streaming
        """
        endpoint = 'v1/events'
        return self.run(endpoint, params=params)


class Streamer(EndpointsMixin, object):
    """ Provides functionality for HTTPS Streaming
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
            self.api_url = 'https://stream-fxpractice.oanda.com'
        elif environment == 'live':
            self.api_url = 'https://stream-fxtrade.oanda.com'
        else:
            raise BadEnvironment(environment)

        self.access_token = access_token
        self.client = requests.Session()
        self.client.stream = True
        self.connected = False

        # personal token authentication
        if self.access_token:
            self.client.headers['Authorization'] = 'Bearer '+self.access_token

    def start(self, ignore_heartbeat=True, **params):
        """ This method only serves backwards compatibility with the
            pre-EndpointsMixin version that only streamed prices
        """
        warnings.warn("Streamer() supports the use of multiple endpoints "
                      "use the rates() method instead",
                      stacklevel=2)
        params['ignore_heartbeat'] = ignore_heartbeat
        self.run("v1/prices", params=params)

    def run(self, endpoint, params=None):
        """ Starts the stream with the given parameters
        :param ignore_heartbeat: (optional) Whether or not to display the
         heartbeat. Default: True
        """
        self.connected = True

        params = params or {}

        ignore_heartbeat = None
        if "ignore_heartbeat" in params:
            ignore_heartbeat = params['ignore_heartbeat']

        request_args = {}
        request_args['params'] = params

        url = '%s/%s' % (self.api_url, endpoint)

        while self.connected:
            response = self.client.get(url, **request_args)

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


class StreamerError(Exception):
    def __init__(self, msg):
        super(StreamerError, self).__init__(msg)
