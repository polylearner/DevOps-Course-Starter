import requests
import json
import os
import pymongo

from todo_app.data.item import Item
from todo_app.data.trelloList import TrelloList
import todo_app.data.trello_constants as constants
import iso8601

class Mongo_service(object):
    trello_lists = {}
     
    def get_mongo_params(self):
        return { 'user_name': os.getenv('USER_NAME'), 
                'password': os.getenv('PASSWORD'),
                'mongo_url': os.getenv('MONGO_URL'),
                'default_db': os.getenv('DEFAULT_DATABASE')}

    def initiate(self):
        self.trello_lists = {}
        mongo_config = self.get_mongo_params()
        mongo_user = mongo_config ['user_name']
        mongo_password = mongo_config ['password']
        mongo_url = mongo_config ['mongo_url']
        mongo_db = mongo_config ['default_db']
        mongo_client = pymongo.MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_url}/{mongo_db}?retryWrites=true&w=majority")
        self.db = mongo_client['mmce_corndel_todo']

    def get_lists(self):
        """
        Fetches all lists from Mongo db.

        """
        lists = self.db.todo_lists.find({})
        for list in lists:
            trelloListDict = TrelloList(name=list[constants.TRELLO_NAME], 
                                        boardId=list[constants.TRELLO_ID_BOARD])
            self.trello_lists[list[constants.TRELLO_ID]] = trelloListDict

    def get_list_id(self, name):
        """
        Get a trello list id for a give name from the list of all lists.

        Returns:
            listId:  The identifier for a given name
        """
        for listId in self.trello_lists:
            trello_list = self.trello_lists[listId]
            if trello_list.name == name:
                return listId

    def get_items_from_trello(self):
        """
        Fetches all saved items from Trello.

        Returns:
            list: The list of saved items.
        """
        items = []
        cards = self.db.cards.find({})
        for card in cards:
            trelloListDict = self.trello_lists[card[constants.TRELLO_IDLIST]]
            item = Item(id=card[constants.TRELLO_ID], 
                        status=trelloListDict.name, 
                        title=card[constants.TRELLO_NAME], 
                        listId=card[constants.TRELLO_IDLIST],
                        lastActivity=iso8601.parse_date(card["dateLastActivity"] ))
            items.insert(1, item)
        return items

    def get_items(self):
        return self.get_items_from_trello()

    def get_item(self, id):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item.id == id), None)

    def add_item(self, title):
        """
        Adds a new item with the specified title to Trello.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        listId = self.get_list_id(constants.TODO_APP_NOT_STARTED)
        url = f"{constants.TRELLO_API_URL}/cards?{self.TRELLO_CREDENTIALS}&idList={listId}&name={title}"
        
        requests.request("POST", url)
        self.get_items_from_trello()

    def save_item(self, item):
        """
        Updates an existing item at Trello. If no existing item matches the ID of the specified item, nothing is saved.

        Args:
            item: The item to save.
        """
        url = f"{constants.TRELLO_API_URL}cards/{item.id}?{self.TRELLO_CREDENTIALS}&idList={item.listId}"
        requests.request("PUT", url)
        self.get_items_from_trello()

    def remove_item(self, id):
        """
        Delete an existing card in the lists.

        Args:
            id: The item's id to delete.
        """
        item = self.get_item(id)
        url = f"{constants.TRELLO_API_URL}cards/{item.id}?{self.TRELLO_CREDENTIALS}&idList={item.listId}"
        requests.request("DELETE", url)
        self.get_items_from_trello()
    
    def create_board(self, name):
        """
        Create a board for testing purpose
        """
        url = f"{constants.TRELLO_API_URL}boards/?{self.TRELLO_CREDENTIALS}&name={name}"
        response = requests.request("POST", url)
        responseText =  response.text
        newBoard = json.loads(responseText.encode('utf8'))
        return newBoard['id']

    def delete_board(self, id):
        """
        Delete a board for testing purpose
        """
        url = f"{constants.TRELLO_API_URL}boards/{id}?{self.TRELLO_CREDENTIALS}"
        response = requests.request("DELETE", url)

def sendRequest(verb, url):
    return requests.request(verb, url)
