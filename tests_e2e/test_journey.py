from time import sleep
from selenium.webdriver.common.by import By
import pytest 

def test_check_title(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

def test_add_todo_item(driver, test_app):
    driver.get('http://localhost:5000/')
    text = "Test 1 To Do Item"

    populate_title_input_element(driver, text)
    submit_title_button_element(driver)

    newToDoItemXPath = '//*[@id="todo_title"]'
    newToDoItem = driver.find_elements(By.XPATH, newToDoItemXPath)
 
    for item in newToDoItem:
        if item.text == text:
            assert item.text == text
            break

def test_change_todo_item_doing(driver, test_app):
    driver.get('http://localhost:5000/')
    text = "Test 2 To Do Item"
    populate_title_input_element(driver, text)
    submit_title_button_element(driver)
    submit_doing_button_element(driver)

    doingToDoItemXPath = '//*[@id="doing_title"]'
    doingToDoItem = driver.find_elements(By.XPATH, doingToDoItemXPath)

    for item in doingToDoItem:
        if item.text == text:
            assert item.text == text
            break

def test_change_todo_item_done(driver, test_app):
    driver.get('http://localhost:5000/')
    text = "Test 3 To Do Item"
    populate_title_input_element(driver, text)
    submit_title_button_element(driver)
    submit_doing_button_element(driver)
    submit_done_button_element(driver)

    doneItemXPath = '//*[@id="recently_done_title"]'
    doneItem = driver.find_elements(By.XPATH, doneItemXPath)

    for item in doneItem:
        if item.text == text:
            assert item.text == text
            break


def populate_title_input_element(driver, text):
    titleInputXPath = "//*[@id=\"title\"]"
    titleInput = driver.find_elements(By.XPATH, titleInputXPath)
    titleInput[0].send_keys(text)
    sleep(1)

def submit_title_button_element(driver):
    titleSubmitXPath = "//*[@id=\"titleSubmit\"]"
    titleSubmit = driver.find_elements(By.XPATH, titleSubmitXPath)
    titleSubmit[0].click()
    sleep(1)

def submit_doing_button_element(driver):
    doingSubmitXPath = "//*[@id=\"SubmitDoing\"]"
    doingSubmit = driver.find_elements(By.XPATH, doingSubmitXPath)
    doingSubmit[0].click()
    sleep(1)

def submit_done_button_element(driver): 
    doneSubmitXPath = "/html/body/div/div[2]/div[2]/div/ul[2]/div/li/ul/div/div[3]/div/form/input"
    doneSubmit = driver.find_elements(By.XPATH, doneSubmitXPath)
    doneSubmit[0].click()
    sleep(1)