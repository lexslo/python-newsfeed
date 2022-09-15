# test signup()
import json
from unittest.mock import patch, MagicMock
from app.models import User, Post, Comment, Vote

# case of successful signup
@patch("app.db.get_db")
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


