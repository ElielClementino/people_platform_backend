from django.contrib.auth.models import User
from model_bakery import baker
import fixtures
import json


def test_must_not_return_logged_user(client):
    resp = client.get("/api/accounts/whoami")

    assert resp.status_code == 200
    assert resp.json() == {"authenticated": False}


def test_must_return_logged_user(client, db):
    fixtures.user_unknown()

    client.force_login(User.objects.get(username="unknown"))
    resp = client.get("/api/accounts/whoami")

    data = resp.json()
    assert resp.status_code == 200
    assert data == {
        "user": {
            "id": 1,
            "name": "user unknown",
            "username": "unknown",
            "first_name": "user",
            "last_name": "unknown",
            "email": "unknown@example.com",
            "permissions": {"ADMIN": False, "STAFF": False},
        },
        "authenticated": True,
    }


def test_must_log_in(client, db):
    fixtures.user_unknown()

    resp = client.post("/api/accounts/login", {"username": "unknown", "password": "unknown"})
    login = resp.json()

    resp = client.get("/api/accounts/whoami")
    data = resp.json()

    assert login["email"] == "unknown@example.com"
    assert resp.status_code == 200
    assert data == {
        "user": {
            "id": 1,
            "name": "user unknown",
            "username": "unknown",
            "first_name": "user",
            "last_name": "unknown",
            "email": "unknown@example.com",
            "permissions": {"ADMIN": False, "STAFF": False},
        },
        "authenticated": True,
    }


def test_must_log_out(client, db):
    fixtures.user_unknown()
    client.force_login(User.objects.get(username="unknown"))
    logged = client.get("/api/accounts/whoami")

    assert logged.json()['authenticated'] is True

    resp = client.post("/api/accounts/logout")

    assert resp.status_code == 200
    assert not resp.json()


def test_not_registering_if_equal_username(client, db):
    baker.make(User, username="unknown", password="unknown")

    new_user = {"userInfo": { "username": "unknown", "email":"unknown@example.com", "password": "unknown"}}

    response = client.post("/api/accounts/register", new_user, content_type="application/json")
    data = json.loads(response.content.decode())


    assert response.status_code == 200
    assert data == {'erro': 'nome de usuário já está sendo usado'}


def test_not_registering_if_equal_email(client, db):
    baker.make(User, username="unknown", password="unknown", email="unknown@example.com")

    new_user = {"userInfo": { "username": "user2", "email":"unknown@example.com", "password": "user2"}}

    response = client.post("/api/accounts/register", new_user, content_type="application/json")
    data = json.loads(response.content.decode())


    assert response.status_code == 200
    assert data == {'erro': 'email já está sendo usado'}


def test_user_registering_is_working(client, db):
    new_user = {"userInfo": { "username": "unknown", "email":"unknown@example.com", "password": "unknown"}}

    response = client.post("/api/accounts/register", new_user, content_type="application/json")
    data = json.loads(response.content.decode())

    assert response.status_code == 200
    assert data == {'sucesso': f'usuário { new_user["userInfo"]["username"] }, sua conta foi criada com sucesso '}