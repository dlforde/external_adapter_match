from adapter import Adapter

data = {
    'football-data':{'endpoint': 'outcome', 'match_id': 3},
    'api-football':{'match_id': 202},
}
input = {
    'id': 1,
    'data': data
}
adapter = Adapter(input)
print(adapter.result)