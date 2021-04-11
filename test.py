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



# curl -d '{"id":2,"data":{"football-data":{"endpoint":"outcome","match_id":3}, "api-football": {"match_id": 202}}}' -H 'Content-Type: application/json' https://658h5tqhxi.execute-api.us-east-2.amazonaws.com/default
