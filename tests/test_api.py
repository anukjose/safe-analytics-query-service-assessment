"""
Tests API behaviour
"""

from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_query_endpoint_success():

    response = client.post("/query", json={"group_by": "department"})

    assert response.status_code == 200

    assert isinstance(response.json(), dict)


def test_query_endpoint_missing_groupby():

    response = client.post("/query", json={})

    assert response.status_code == 422


def test_query_endpoint_invalid_groupby():

    response = client.post("/query", json={"group_by": "unknown"})

    assert response.status_code == 400

    assert "error" in response.json()

    assert response.json()["error"] == "Invalid group_by field: unknown"


def test_query_endpoint_invalid_filter():

    response = client.post(
        "/query",
        json={"group_by": "department", "filter": {"unknown_column": "London"}},
    )

    assert response.status_code == 400

    assert "error" in response.json()

    assert response.json()["error"] == "Invalid filter column: unknown_column"


def test_query_endpoint_with_filter():

    response = client.post(
        "/query", json={"group_by": "department", "filter": {"location": "London"}}
    )

    assert response.status_code == 200

    assert isinstance(response.json(), dict)
