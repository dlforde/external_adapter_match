import json



class FootballDataClient:

    def __init__(self):
        self.source = 'football-data'
        self.base_url = 'https://api.football-data.org/v2/'
        with open('./config/accounts.json') as file:
            accounts = json.load(file)
            self.api_key = accounts[self.source]['api_key']


    def get_match(self, data, bridge):
        """
        Ping API to obtain match data
        """
        headers = {'X-Auth-Token': self.api_key}
        url = self.base_url + 'matches/{match_id}'.format(match_id = data['match_id'])
        if data['endpoint'] == 'outcome':
            response = bridge.request(url, headers = headers)
            response = response.json()
            winner = response['match']['score']['winner']

            if winner == 'HOME_TEAM':
                result = 1
            elif winner == 'DRAW':
                result = 2
            elif winner == 'AWAY_TEAM':
                result = 3
            else:
                result = 0

        return result
