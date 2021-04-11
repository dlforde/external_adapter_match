from lib.bridge import Bridge
from connectors.football_data import FootballDataClient
from connectors.api_football import ApiFootballClient

class Adapter:

    def __init__(self, input):
        # id should always be supplied by Chainlink node; if not defaults to 1
        self.id = input.get('id', '1')
        self.request_data = input.get('data')
        if self.validate_request_data():
            self.bridge = Bridge()
            self.create_request()
        else:
            self.result_error('No data provided')


    def validate_request_data(self):
        """
        Check valid data has been passed in request payload
        """
        if self.request_data is None:
            return False
        if self.request_data == {}:
            return False
        return True


    def create_request(self):
        """
        Make request to obtain data
        """
        try:
            # putting calls to both apis here
            data = {}

            # football-data
            request_data = self.request_data['football-data']
            football_data_client = FootballDataClient()
            data['football-data'] = football_data_client.get_match(request_data, self.bridge)

            # api-football
            request_data = self.request_data['api-football']
            api_football_client = ApiFootballClient()
            data['api-football-api'] = api_football_client.get_match(request_data, self.bridge)

            # resolve final output
            if data['football-data'] != data['api-football-api']:
                result = None
            else:
                result = data['football-data']

            self.result = result
            data['result'] = self.result
            self.result_success(data)
        except Exception as e:
            self.result_error(e)
        finally:
            self.bridge.close()


    def result_success(self, data):
        """
        Set return value of successful call
        """
        self.result = {
            'jobRunID': self.id,
            'data': data,
            'result': self.result,
            'statusCode': 200
        }


    def result_error(self, error):
        """
        Set return value of unsuccessful call
        """
        self.result = {
            'jobRunID': self.id,
            'status': 'errored',
            'error': f'There was an error: {error}',
            'statusCode': 500
        }
