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
    os.environ['DEFAULT_DATABASE'] = 'mmce_corndel_todo_test'
    service.initiate()
    board_id = service.create_board("E2E Test board")
    os.environ['MONGO_BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    application.config['LOGIN_DISABLED'] = True
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1)
    service.delete_board(board_id)


