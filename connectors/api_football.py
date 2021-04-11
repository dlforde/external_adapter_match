import json



class ApiFootballClient:

    def __init__(self):
        self.source = 'api-football'
        #self.base_url = 'https://v3.football.api-sports.io/'
        self.base_url = 'https://api-football-v1.p.rapidapi.com/v3/'
        with open('./config/accounts.json') as file:
            accounts = json.load(file)
            self.api_key = accounts[self.source]['api_key']

        with open('./config/api_football_teams.json') as teams:
            self.teams = json.load(teams)

    def get_match(self, data, bridge):
        """
        Ping API to obtain match data
        """

        split_strings = data[-6:]
        gameweek = int(split_strings[0:2],16)
        hometeam = int(split_strings[2:4],16)
        awayteam = int(split_strings[4:6],16)

        url = self.base_url + 'fixtures'
        params = {
            "league":"39",
            "season":"2020",
            "round":"Regular Season - %s" % gameweek
        }
        headers = {
            #'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        }


        response = bridge.request(url, params = params, headers = headers)
        response = response.json()['response']
        # print(response['fixture']['status'])
        # print(response['teams'])
        # print(response['goals'])

        result = 0

        for match in response:
            if self.teams[hometeam] == match['teams']['home']['name'] and self.teams[awayteam] == match['teams']['away']['name']:
                if match['fixture']['status']['short'] != 'FT':
                    result = 0
                elif match['teams']['home']['winner']:
                    result = 1
                elif match['teams']['away']['winner']:
                    result = 3
                else:
                    result = 2

        return result
