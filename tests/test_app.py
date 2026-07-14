from fastapi.testclient import TestClient

from src import app as app_module


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app_module.app)

    response = client.delete(
        "/activities/Chess%20Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_rejects_when_activity_is_full():
    client = TestClient(app_module.app)
    activity = app_module.activities["Chess Club"]
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "overflow@mergington.edu"},
    )

    assert response.status_code == 400
    assert "full" in response.json()["detail"].lower()
