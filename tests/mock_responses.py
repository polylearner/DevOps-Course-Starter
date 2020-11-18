import io

class MockListsResponse(object):
    def __init__(self):
        self.status_code = 200
        self.url = 'http://httpbin.org/get'
        self.headers = {'blaa': '1234'}

    @property
    def text(self):
        with io.open("tests/trello_resp_list.json") as f:
            content = f.read()
        return content

class MockCardsResponse(object):
    def __init__(self):
        self.status_code = 200
        self.url = 'http://httpbin.org/get'
        self.headers = {'blaa': '1234'}

    @property
    def text(self):
        with io.open("tests/trello_resp_cards.json") as f:
            content = f.read()
        return content