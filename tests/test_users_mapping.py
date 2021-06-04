from todo_app.data import user_role
import pytest
from dotenv import load_dotenv, find_dotenv

@pytest.fixture()
def loadfile():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

def test_reader_role(loadfile):
    isUserReader = user_role.isReaderRole('123456788')

    assert isUserReader == True

def test_writer_role(loadfile):
    isUserWriter = user_role.isWriterRole('123456789')

    assert isUserWriter ==True