import json



class ApiFootballClient:

    def __init__(self):
        self.source = 'api-football'
        #self.base_url = 'https://v3.football.api-sports.io/'
        self.base_url = 'https://api-football-v1.p.rapidapi.com/v3/'
        with open('./config/accounts.json') as file:
            accounts = json.load(file)
            self.api_key = accounts[self.source]['api_key']


    def get_match(self, data, bridge):
        """
        Ping API to obtain match data
        """
        url = self.base_url + 'fixtures'
        params = {
            'id': data['match_id']
        }
        headers = {
            #'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        }
        response = bridge.request(url, params = params, headers = headers)
        response = response.json()['response'][0]
        # print(response['fixture']['status'])
        # print(response['teams'])
        # print(response['goals'])

        # skip if match not finished
        if response['fixture']['status']['short'] != 'FT':
            result = 0
        elif response['teams']['home']['winner']:
            result = 1
        elif response['teams']['away']['winner']:
            result = 3
        else:
            result = 2

        return result
