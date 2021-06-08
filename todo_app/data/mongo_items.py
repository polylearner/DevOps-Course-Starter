from datetime import datetime
from typing import Collection
import requests
import json
import os
import pymongo
from bson import ObjectId

from todo_app.data.item import Item
from todo_app.data.mongoList import MongoList
import todo_app.data.mongo_constants as constants
import iso8601

class Mongo_service(object):
    mongo_lists = {}
     
    def get_mongo_params(self):
        return { 'user_name': os.getenv('USER_NAME'), 
                'password': os.getenv('PASSWORD'),
                'mongo_url': os.getenv('MONGO_URL'),
                'default_db': os.getenv('DEFAULT_DATABASE'),
                'mongo_prefix': os.getenv('MONGO_PREFIX')}

    def initiate(self):
        self.mongo_lists = {}
        self.init_mongo_db()

    def init_mongo_db(self):
        mongo_config = self.get_mongo_params()
        mongo_user = mongo_config ['user_name']
        mongo_password = mongo_config ['password']
        mongo_url = mongo_config ['mongo_url']
        mongo_db = mongo_config ['default_db']
        mongo_prefix = mongo_config ['mongo_prefix']
        mongo_client = pymongo.MongoClient(f"{mongo_prefix}{mongo_user}:{mongo_password}@{mongo_url}/{mongo_db}?retryWrites=true&w=majority")
        self.client = mongo_client
        self.db = mongo_client[f'{mongo_db}']

    def get_lists(self):
        """
        Fetches all lists from Mongo db.

        """
        lists = self.db.todo_lists.find({})
        if( lists.collection.count() == 0):
            self.insert_todo_lists()
            lists = self.db.todo_lists.find({})

        for list in lists:
            mongoListDict = MongoList(name=list[constants.MONGO_NAME], 
                                        boardId=list[constants.MONGO_ID])
            self.mongo_lists[list[constants.MONGO_ID]] = mongoListDict

    def get_list_id(self, name):
        """
        Get a mongo list id for a give name from the list of all lists.

        Returns:
            listId:  The identifier for a given name
        """
        for listId in self.mongo_lists:
            mongo_list = self.mongo_lists[listId]
            if mongo_list.name == name:
                return listId

    def get_items_from_mongo(self):
        """
        Fetches all saved items from mongo.

        Returns:
            list: The list of saved items.
        """
        items = []
        cards = self.db.cards.find({})
        for card in cards:
            mongoListDict = self.mongo_lists[card[constants.MONGO_IDLIST]]
            item = Item(id=card["_id"], 
                        status=mongoListDict.name, 
                        title=card[constants.MONGO_NAME], 
                        listId=card[constants.MONGO_IDLIST],
                        lastActivity=iso8601.parse_date(card["dateLastActivity"] ))
            items.insert(1, item)
        return items

    def get_items(self):
        return self.get_items_from_mongo()

    def get_item(self, id):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item.id == ObjectId(id)), None)

    def add_item(self, title):
        """
        Adds a new item with the specified title to mongo.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        listId = self.get_list_id(constants.TODO_APP_NOT_STARTED)
        currentDate = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        cards = self.db.cards
        item = {
            "idList": listId,
            "name": title,
            "dateLastActivity": currentDate
        }
        post_id = cards.insert(item)
        self.get_items_from_mongo()

    def save_item(self, item):
        """
        Updates an existing item at mongo. If no existing item matches the ID of the specified item, nothing is saved.

        Args:
            item: The item to save.
        """
        listId = self.get_list_id(item.status)
        currentDate = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        cards = self.db.cards

        cards.update_one({"_id": item.id}, {"$set":
                 {"idList": listId,
                  "dateLastActivity": currentDate}
             })
        self.get_items_from_mongo()

    def remove_item(self, id):
        """
        Delete an existing card in the lists.

        Args:
            id: The item's id to delete.
        """
        item = self.get_item(id)
        cards = self.db.cards
        cards.delete_one({"_id": item.id})
        self.get_items_from_mongo()
    
    def create_board(self, name, collection):
        """
        Create a board for testing purpose
        """
        self.db = self.client[name]
        self.db.create_collection(collection)
        self.insert_todo_lists()

    def insert_todo_lists(self):
        self.db.todo_lists.insert_many([{
                                        "_id": "60916128ff76116ee04dd66d",
                                        "name": "To Do",
                                        },{
                                        "_id": "60916128ff76116ee04dd66e",
                                        "name": "Doing",
                                        },{
                                        "_id": "60916128ff76116ee04dd66f",
                                        "name": "Done",
                                        }])

    def delete_board(self, name, collection):
        """
        Delete a board for testing purpose
        """
        self.db = self.client[name]
        self.db.drop_collection(collection)
        self.db.drop_collection('cards')

def sendRequest(verb, url):
    return requests.request(verb, url)
