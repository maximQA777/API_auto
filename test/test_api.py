import json
import requests
from jsonschema import validate
from schemas.schemas import get_user, create_user, update_user, register_user

BASE_URL = "https://reqres.in"


# GET tests
def test_get_users_success():
    response = requests.get(f"{BASE_URL}/api/users/2")
    assert response.status_code == 200
    body = response.json()
    validate(body, get_user)


def test_get_user_not_found():
    response = requests.get(f"{BASE_URL}/api/users/QA_quru_test")
    assert response.status_code == 404


# POST tests
def test_create_user_success():
    payload = {"name": "morpheus1", "job": "leader"}
    response = requests.post(f"{BASE_URL}/api/users", json=payload)
    assert response.status_code == 201
    body = response.json()
    validate(body, create_user)


def test_register_user_success():
    payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
    response = requests.post(f"{BASE_URL}/api/register", json=payload)
    assert response.status_code == 200
    body = response.json()
    validate(body, register_user)


def test_register_user_missing_password():
    payload = {"email": "eve.holt@reqres.in"}
    response = requests.post(f"{BASE_URL}/api/register", json=payload)
    assert response.status_code == 400
    body = json.loads(response.text)
    assert body == {"error": "Missing password"}


def test_register_user_missing_emaill():
    payload = {"password":"pistol"}
    response = requests.post(f"{BASE_URL}/api/register", json=payload)
    assert response.status_code == 400
    body = json.loads(response.text)
    assert body == {"error": "Missing email or username"}


# PUT test
def test_update_user_success():
    payload = {"name": "morpheus", "job": "zion resident"}
    response = requests.put(f"{BASE_URL}/api/users/2", json=payload)
    assert response.status_code == 200
    body = response.json()
    validate(body, update_user)


# DELETE test
def test_delete_user_success():
    response = requests.delete(f"{BASE_URL}/api/users/2")
    assert response.status_code == 204