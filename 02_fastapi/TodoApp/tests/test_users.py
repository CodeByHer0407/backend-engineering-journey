from routers.users import get_db, get_current_user
from fastapi import status 
from tests.utils import *
import pytest


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user 


def test_return_user(test_user):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codingwithshizi'
    assert response.json()['email'] == 'codingwithshizibytest@email.com' 
    assert response.json()['first_name'] == 'Shizi'
    assert response.json()['last_name'] == 'Codes'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(91)-111-1111'


def test_change_phone_number_success(test_user):
    response = client.put("/users/phone-number", json={"phone_number": "2222222222"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Phone number updated successfully."
    }
    

def test_change_password_success(test_user):
    response = client.put('/users/password', json={'password': 'testpassword', 'new_password': 'test1234'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "Password updated successfully."
    }

   
def test_change_password_invalid_current_password(test_user):
    response = client.put('/users/password', json={'password': 'wrong_password', 'new_password': 'test1234'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect current password.'}