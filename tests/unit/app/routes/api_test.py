# test signup()
import json
from unittest.mock import patch, MagicMock

from app.db import Session
from app.models import User, Post, Comment, Vote


# case of successful signup
# @patch("app.db.Session")
@patch("app.routes.api.get_db")
def test_signup_success(mock_get_db, client):
    # mock the dependencies
    # use MagicMock to mock db.add(newUser) and db.commit()
    # MagicMock() used for purpose of testing
    mock_get_db.return_value = MagicMock()

    data = {
        "username": "Test Human",
        "email": "test@e.com",
        "password": "password"
    }

    # call the endpoint
    response = client.post(path='/api/users', json=json.dumps(data))

    # ensure there is a response from db
    assert response
    print('Response: ', response)
    # assert that MagicMock object is used
    mock_get_db.assert_called()


@patch("app.routes.api.get_db")
def test_signup_bad_email(mock_get_db, client):
    # mock the dependencies
    # use MagicMock to mock db.add(newUser) and db.commit()
    # MagicMock() used for purpose of testing
    mock_get_db.return_value = MagicMock()

    data = {
        "username": "Test Human",
        "email": "email",
        "password": "password"
    }

    # call the endpoint
    response = client.post(path='/api/users', json=json.dumps(data))

    # ensure there is a response from db
    assert response.status_code == 500
    print('Response: ', response)
    # assert that MagicMock object is used
    mock_get_db.assert_called()

    # assert False

@patch("app.routes.api.get_db")
# goes first in parameters
@patch.object(User, "verify_password")
def test_upvote_success(mock_verify_pw, mock_get_db, client):
    mock = MagicMock()
    # nested mocks
    mock.query.return_value.filter.return_value.one.return_value = User(email = "email@t.co", password = "password123")
    mock_get_db.return_value = mock
    # mock verify_password
    mock_verify_pw.return_value = True
    # mock_db_query.return_value = User(email = "email@t.co")

    # call login endpoint
    email = {
        "email":"email@t.co",
        "password":"password123"
    }
    login = client.post(path='api/users/login', json=json.dumps(email))
    assert login.status_code == 200
    # mock_get_session.return_value = True


    data = {
        "post_id": 333,
        "user_id": 111
    }

    response = client.put(path='api/posts/upvote', json=json.dumps(data))

    assert response.status_code == 200
    print('Response', response)

    mock_get_db.assert_called()
    # mock_get_session.assert_called()



