from django.urls import reverse
from django.test.client import Client
from api.management.commands.app_create_super_admin import Command
from unittest import TestCase
import pytest

specsymbols = ['!','@','#','$','%','^','&','*','(',')','=',"'",'"',':',';','\\','/','?','+','~','`']


def test_ping():
    client = Client()
    response = client.get(reverse("api:ping"), content_type="application/json")
    assert response.status_code == 200
    assert response.json() == {"response": "pong"}


def test_auth_bad_creds():
    client = Client()
    response = client.post(
        reverse("api:auth"),
        content_type="application/json",
        data={
            "engine": "email",
            "credentials": {
                "email": "some@email",
                "password": "StrongPassword",
            },
        },
    )
    assert response.status_code == 401


def test_api_connection():
    client = Client()
    response = client.post(
        reverse("api:auth"),
        content_type="application/json",
        data={"engine": "email",
              "credentials": {
                  "email": "super_admin@example.com",
                  "password": "StrongPass777"
              }
              }
    )
    content = response.json()
    assert response.status_code == 200
    assert content["user"]["first_name"] == "admin"


@pytest.mark.parametrize("first_name, last_name, email, password",
                         [
                             ('TestSuper', 'Admin', 'test@test.com', '#*^#*@:bad'),
                             ('TestSuper', 'Admin', 'test@test.test', 'Good_password')
                         ]
                         )
def test_superuser_creation(first_name, last_name, email, password):
    case = TestCase()
    first_name = first_name
    last_name = last_name
    email = email
    password = password
    cmd = Command()
    user = cmd.handle(first_name=first_name,
                      last_name=last_name,
                      email=email,
                      password=password
                      )
    assert len(user.validate_name('email', email).split()) == 1
    assert all(specsymbol not in password for specsymbol in specsymbols), 'Password should not contain specsymbols'
    assert user.is_confirmed is True


@pytest.mark.xfail
def test_user_creation_fail():
    cmd = Command()
    user = cmd.handle(first_name='TestSuper',
                      last_name='Admin',
                      email='fortest-test.com',
                      password='Good_password'
                      )

def test_handbooks_created():
    client = Client()
    response = client.get('/api/handbooks')
    content = response.json()
    assert response.status_code == 200
    assert content['configs'][1]['value'] == 43200
