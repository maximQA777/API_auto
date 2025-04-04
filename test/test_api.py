import json
import pytest
import requests
from jsonschema import validate
from schemas.schemas import get_user, create_user, update_user, register_user

BASE_URL = "https://reqres.in"


# Тесты GET запросов
def test_get_users_success():
    """Проверяем успешное получение пользователя по ID"""
    response = requests.get(f"{BASE_URL}/api/users/2")
    assert response.status_code == 200
    body = response.json()
    validate(body, get_user)


def test_get_user_not_found():
    """Проверяем получение 404 при запросе несуществующего пользователя"""
    # Исправлено: теперь используем несуществующий числовой ID вместо строки
    response = requests.get(f"{BASE_URL}/api/users/999999")
    assert response.status_code == 404


# Тесты POST запросов
def test_create_user_success():
    # Создаем пользователя
    payload = {"name": "morpheus1", "job": "leader"}
    response = requests.post(f"{BASE_URL}/api/users", json=payload)
    assert response.status_code == 201
    body = response.json()
    validate(body, create_user)



def test_register_user_success():
    """Проверяем успешную регистрацию пользователя"""
    payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
    response = requests.post(f"{BASE_URL}/api/register", json=payload)
    assert response.status_code == 200
    body = response.json()
    validate(body, register_user)


@pytest.mark.parametrize("payload,expected_error", [
    ({"email": "eve.holt@reqres.in"}, {"error": "Missing password"}),
    ({"password": "pistol"}, {"error": "Missing email or username"})
])
def test_register_user_missing_fields(payload, expected_error):
    """Параметризованный тест для проверки регистрации с отсутствующими полями"""
    # Объединили два теста в один параметризованный
    response = requests.post(f"{BASE_URL}/api/register", json=payload)
    assert response.status_code == 400
    body = json.loads(response.text)
    assert body == expected_error


# Тест PUT запроса
def test_update_user_success():
    """Проверяем успешное обновление пользователя"""
    # Сначала создаем тестового пользователя
    create_payload = {"name": "test_user", "job": "tester"}
    create_response = requests.post(f"{BASE_URL}/api/users", json=create_payload)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    try:
        # Обновляем данные пользователя
        update_payload = {"name": "updated_user", "job": "qa engineer"}
        response = requests.put(f"{BASE_URL}/api/users/{user_id}", json=update_payload)
        assert response.status_code == 200
        body = response.json()
        validate(body, update_user)
        assert body["name"] == update_payload["name"]
        assert body["job"] == update_payload["job"]
    finally:
        # Удаляем тестового пользователя после выполнения теста
        requests.delete(f"{BASE_URL}/api/users/{user_id}")


# Тест DELETE запроса
def test_delete_user_success():
    """Проверяем успешное удаление пользователя"""
    # Сначала создаем пользователя для удаления
    create_payload = {"name": "temp_user", "job": "temp"}
    create_response = requests.post(f"{BASE_URL}/api/users", json=create_payload)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Удаляем пользователя
    response = requests.delete(f"{BASE_URL}/api/users/{user_id}")
    assert response.status_code == 204

    # Проверяем, что пользователь действительно удален
    get_response = requests.get(f"{BASE_URL}/api/users/{user_id}")
    assert get_response.status_code == 404