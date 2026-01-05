import pytest
from app import app

app.config.update({
    "TESTING": True,
    })

def test_homepage():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b'Create an account!' in response.data