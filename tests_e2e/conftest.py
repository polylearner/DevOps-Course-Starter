import os
from attr import setters
from dotenv import load_dotenv, find_dotenv
import pytest
from threading import Thread
from selenium import webdriver

from todo_app.data.mongo_items import Mongo_service as Service
from todo_app import app
from selenium import webdriver

@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver

@pytest.fixture(scope="module")
def test_app(driver):
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    # Create the new board & update the board id environment variable
    service = Service()
    db_name = 'mmce_corndel_todo_test'
    test_collection = 'todo_lists'
    os.environ['DEFAULT_DATABASE'] = db_name
    service.initiate()
    service.create_board(db_name, test_collection)
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    service.delete_board(name=db_name, collection=test_collection)


