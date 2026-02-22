from urllib.parse import quote


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    unregister_url = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    unregister_response = client.delete(unregister_url, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    unregister_url = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    response = client.delete(unregister_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-enrolled@mergington.edu"
    unregister_url = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    response = client.delete(unregister_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
