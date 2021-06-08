import os
from dotenv import load_dotenv, find_dotenv
import pymongo
import pytest
from todo_app import app
import mongomock

@pytest.fixture()
def client():
    with mongomock.patch(servers=(("tst.mongo.test", 27017),)) as mongodb:
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)
        # Use our test integration config instead of the 'real' version
        # Create the new app.

        prepareMockMongo()
        test_app = app.create_app()
        test_app.config['LOGIN_DISABLED'] = True
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

def prepareMockMongo():
        data_lists = [{"_id": "60916128ff76116ee04dd66d",
                        "id": "5f6456f870c89e025d4cb788",
                        "name": "To Do",
                        "closed": "false",
                        "idBoard": "5f6456f8fc414517ed9b0e41",
                        "subscribed": "false"
                        },{
                        "_id": "60916128ff76116ee04dd66e",
                        "id": "5f898ae720d5bc2a631ce2e1",
                        "name": "Doing",
                        "closed": "false",
                        "idBoard": "5f6456f8fc414517ed9b0e41",
                        "subscribed": "false"
                        },{
                        "_id": "60916128ff76116ee04dd66f",
                        "id": "5f6456f8536a55223a9ebca0",
                        "name": "Done",
                        "closed": "false",
                        "idBoard": "5f6456f8fc414517ed9b0e41",
                        "subscribed": "false"
                        }]

        data_cards = [{"_id":"5f6a132be45bd103bdaa16a9","idList":"5f6456f8536a55223a9ebca0","name":"test sunday","dateLastActivity":"2021-05-06T07:46:01.741080Z"}]
        client = pymongo.MongoClient("tst.mongo.test")
        client.mmce_corndel_todo_test.todo_lists.insert_many(data_lists)
        client.mmce_corndel_todo_test.cards.insert_many(data_cards)