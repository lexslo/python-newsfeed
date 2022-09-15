# Conftest is a file that is shared among all tests
import pytest
from app import app

from flask import Flask
# import sqlalchemy

# Fixture: object that can be called from the tests

@pytest.fixture
def flask_app_mock():
    app_mock = Flask(__name__)
    db = sqlalchemy(app_mock)
    db.init_app(app_mock)
    return app_mock

# @pytest.fixture
# def mock_get_sqlalchemy(mocker):
#     mock = mocker.patch("SQLAlchemy._QueryProperty.__get__").return_value = mocker.Mock()
#     return mock

@pytest.fixture
def client():
    with app.test_client() as test_client:
        yield test_client
