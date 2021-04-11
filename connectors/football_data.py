import json



class FootballDataClient:

    def __init__(self):
        self.source = 'football-data'
        self.base_url = 'https://api.football-data.org/v2/'
        with open('./config/accounts.json') as file:
            accounts = json.load(file)
            self.api_key = accounts[self.source]['api_key']

        with open('./config/football_data_teams.json') as teams:
            self.teams = json.load(teams)



    def get_match(self, data, bridge):
        """
        Ping API to obtain match data
        """

        split_strings = data[-6:]
        gameweek = int(split_strings[0:2],16)
        hometeam = int(split_strings[2:4],16)
        awayteam = int(split_strings[4:6],16)

        headers = {'X-Auth-Token': self.api_key}

        url = self.base_url + 'competitions/PL/matches?matchday=%s' % gameweek
        response = bridge.request(url, headers = headers)
        response = response.json()['matches']

        result=0

        for x in response:
            if self.teams[hometeam] == x['homeTeam']['name'] and self.teams[awayteam] == x['awayTeam']['name']:
                winner = x['score']['winner']
                if winner == 'HOME_TEAM':
                    result = 1
                elif winner == 'DRAW':
                    result = 2
                elif winner == 'AWAY_TEAM':
                    result = 3
                else:
                    result = 0

        return result
