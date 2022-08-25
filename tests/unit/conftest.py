# Conftest is a file that is shared among all tests
import pytest
from app import app
# Fixture: object that can be called from the tests

@pytest.fixture
def client():
    with app.test_client() as test_client:
        yield test_client
