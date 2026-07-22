from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert email in response.json()["participants"]

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert email not in response.json()["participants"]


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"
