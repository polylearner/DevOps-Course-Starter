import vcr
import json
import os, requests
from todo_app.data.trello_constants import TRELLO_API_URL

def get_auth_params():
    return { 'key': os.getenv('TRELLO_KEY'), 
            'token': os.getenv('TRELLO_TOKEN'),
            'list': os.getenv('TRELLO_BOARD_ID')}
            
trello_config = get_auth_params()
trello_key = trello_config ['key']
trello_token = trello_config ['token']
trello_default_board = trello_config ['list']
trello_credentials = f"key={trello_key}&token={trello_token}"

urlDict = { "getLists" : f"{TRELLO_API_URL}boards/{trello_default_board}/lists?{trello_credentials}",
            "getItems" :f"{TRELLO_API_URL}boards/{trello_default_board}/cards?{trello_credentials}" }

def test_getLists():
    with vcr.use_cassette('vcr_cassettes/get_lists_recording.yaml'):
        response = requests.get(urlDict['getLists'])
        assert response.status_code == 200
        if response.status_code == 200:
            responseText =  response.text
            raw_lists = (json.loads(responseText.encode('utf8'))) 
            assert len(raw_lists) == 3
            assert raw_lists[0]['name'] == 'To Do'
            assert raw_lists[1]['name'] == 'Doing'
            assert raw_lists[2]['name'] == 'Done'

def test_getItems():
    with vcr.use_cassette('vcr_cassettes/get_items_recording.yaml'):
        response = requests.get(urlDict['getItems'])
        assert response.status_code == 200
        if response.status_code == 200:
            responseText =  response.text
            raw_lists = (json.loads(responseText.encode('utf8'))) 
            assert len(raw_lists) > 0