def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity(client):
    email = "test_student@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Confirm the student is now in the participants list
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_is_rejected(client):
    email = "duplicate@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_from_activity(client):
    email = "test_remove@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})

    response = client.delete("/activities/Chess Club/unregister", params={"email": email})
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_found_returns_404(client):
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "any@mergington.edu"})
    assert response.status_code == 404


def test_unregister_nonparticipant_returns_404(client):
    response = client.delete("/activities/Chess Club/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
