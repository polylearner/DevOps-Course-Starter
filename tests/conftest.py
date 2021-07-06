import os
from dotenv import load_dotenv, find_dotenv
import pymongo
import pytest
from todo_app import app
import mongomock

@pytest.fixture()
def client():
    with mongomock.patch(servers=(("mmce_devops_sa.tst.mongo.test", 27017),)) as mongodb:
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)
        # Use our test integration config instead of the 'real' version
        # Create the new app.

        prepareMockMongo()
        test_app = app.create_app()
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

def prepareMockMongo():
        data_lists = [{"_id":"60916128ff76116ee04dd66d","name":"To Do"},{"_id":"60916128ff76116ee04dd66e","name":"Doing"},{"_id":"60916128ff76116ee04dd66f","name":"Done"}]
        data_cards = [{"_id":"5f6a132be45bd103bdaa16a9","idList":"60916128ff76116ee04dd66d","name":"test sunday","dateLastActivity":"2021-05-06T07:46:01.741080Z"}]
        client = pymongo.MongoClient("mmce_devops_sa.tst.mongo.test")
        client.mmce_corndel_todo_test.todo_lists.insert_many(data_lists)
        client.mmce_corndel_todo_test.cards.insert_many(data_cards)