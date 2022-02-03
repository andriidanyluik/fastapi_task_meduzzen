import json

import pytest

from app.api import services


def test_create_user(test_app, monkeypatch):
    test_data = {"user_name": "Jonh", "email": "Jonh@gmail.com", "id": 2, "password": "123"}

    def mock_post(db_session, payload):
        return test_data

    monkeypatch.setattr(services, "post", mock_post)

    response = test_app.post("/users/", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_data


def test_create_user_invalid_json(test_app):
    response = test_app.post("/users/", data=json.dumps({"users": "something"}))
    assert response.status_code == 422

    response = test_app.post(
        "/users/", data=json.dumps({"user_nane": "1", "email": "2", 'password': '123'})
    )
    assert response.status_code == 422


def test_read_user(test_app, monkeypatch):
    test_data = {"user_name": "Andrii", "email": "and@gmail.com", "id": 2, 'password': '123'}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(services, "get", mock_get)

    response = test_app.get("/users/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_user_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(services, "get", mock_get)

    response = test_app.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/users/0")
    assert response.status_code == 422


def test_read_all_users(test_app, monkeypatch):
    test_data = [
        {"user_name": "Andrii", "email": "and@gmail.com", "id": 1, 'password': '123'},
        {"user_name": "someone", "email": "someone else", "id": 2, 'password': '123'},
    ]

    def mock_get_all(db_session):
        return test_data

    monkeypatch.setattr(services, "get_all", mock_get_all)

    response = test_app.get("/users/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_user(test_app, monkeypatch):
    test_data = {"user_name": "Andrii", "email": "and@gmail.com", "id": 1, "password": "123"}
    test_update_data = {"user_name": "Andrew", "email": "andrew@ukr.net", "id": 1, "password": "123"}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(services, "get", mock_get)

    def mock_put(db_session, user, user_name, email, password):
        return test_update_data

    monkeypatch.setattr(services, "put", mock_put)

    response = test_app.put("/users/1/", data=json.dumps(test_update_data),)
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"email": "bar"}, 422],
        [999, {"user_name": "foo", "email": "bar", "password": "123"}, 404],
        [1, {"user_name": "1", "email": "bar", "password": "123"}, 422],
        [1, {"user_name": "foo", "email": "1", "password": "123"}, 422],
        [0, {"user_name": "foo", "email": "bar", "password": "123"}, 422],
    ],
)
def test_update_user_invalid(test_app, monkeypatch, id, payload, status_code):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(services, "get", mock_get)

    response = test_app.put(f"/users/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_user(test_app, monkeypatch):
    test_data = {"user_name": "Andrew", "email": "andrew@ukr.net", "id": 1, 'password': '123'}

    def mock_get(db_session, id):
        return test_data

    monkeypatch.setattr(services, "get", mock_get)

    def mock_delete(db_session, id):
        return test_data

    monkeypatch.setattr(services, "delete", mock_delete)

    response = test_app.delete("/users/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_user_incorrect_id(test_app, monkeypatch):
    def mock_get(db_session, id):
        return None

    monkeypatch.setattr(services, "get", mock_get)

    response = test_app.delete("/users/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/users/0/")
    assert response.status_code == 422
