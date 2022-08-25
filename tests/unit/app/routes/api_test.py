# test signup()
import json
from unittest.mock import patch, MagicMock


# case of successful signup
@patch("app.routes.api.get_db")
def test_signup_success(mock_get_db, client):
    # mock the dependencies
    # use MagicMock to mock db.add(newUser) and db.commit()
    mock_get_db.return_value = MagicMock()

    data = {
        "username": "Test Human",
        "email": "test@e.com",
        "password": "password"
    }

    # call the endpoint
    response = client.post(path='/users', data=json.dumps(data))

    # ensure there is a response
    assert response


