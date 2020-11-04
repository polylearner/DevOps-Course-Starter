import vcr
import json
import os, requests
from todo_app.data.trello_constants import TRELLO_API_URL
import todo_app.data.trello_items as trello_items

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
    with vcr.use_cassette('vcr_cassettes/get_lists_recording.yaml') as cass:
        response = requests.get(urlDict['getLists'])
        assert response.status_code == 200
        if response.status_code == 200:
            responseText =  response.text
            raw_lists = (json.loads(responseText.encode('utf8'))) 
            assert len(raw_lists) == 3
            assert raw_lists[0]['name'] == 'To Do'
            assert raw_lists[1]['name'] == 'Doing'
            assert raw_lists[2]['name'] == 'Done'
            cass.rewind()

def test_getItems():
    with vcr.use_cassette('vcr_cassettes/get_items_recording.yaml') as cass:
        response = requests.get(urlDict['getItems'])
        assert response.status_code == 200
        if response.status_code == 200:
            responseText =  response.text
            raw_lists = (json.loads(responseText.encode('utf8'))) 
            assert len(raw_lists) > 0
            cass.rewind()

def test_get_lists_from_trello():
    service = trello_items.Trello_service()
    service.initiate()
    with vcr.use_cassette('vcr_cassettes/get_lists_recording.yaml') as cass:
        service.get_lists()
        listId = service.get_list_id('To Do')
        assert listId != None
        cass.rewind()
    
def test_get_items_from_trello():
    service = trello_items.Trello_service()
    service.initiate()
    with vcr.use_cassette('vcr_cassettes/get_lists_recording.yaml') as cass:
        service.get_lists()
        cass.rewind()
        
    with vcr.use_cassette('vcr_cassettes/get_items_recording.yaml') as cass:
        items = service.get_items()
        assert len(items) > 0
        cass.rewind()

