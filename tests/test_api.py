from django.urls import reverse
from django.test.client import Client
import requests


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
        data = {"engine": "email",
                "credentials": {
                    "email": "super_admin@example.com",
                    "password": "StrongPass777"
                   }
            }
    )
    content = response.json()
    assert response.status_code == 200
    assert content["user"]["first_name"] == "admin"


# TODO дописать тесты
#@pytest.mark.parametrize()
# def test_user_registration():
#     client = Client()
#     response = client.post(
#         reverse("api:auth"),
#         content_type="application/json",
#         data={
#
#         }
#     )
