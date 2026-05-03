import pytest
from fastapi.testclient import TestClient


def test_get_activities(client: TestClient):
    """Test GET /activities returns all activities with details."""
    # Arrange: No special setup needed, activities are in-memory

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status and response structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_signup_success(client: TestClient):
    """Test successful signup for an activity."""
    # Arrange: Choose an activity and new email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]


def test_signup_duplicate(client: TestClient):
    """Test signup fails for duplicate email."""
    # Arrange: Sign up first
    activity_name = "Programming Class"
    email = "duplicate@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: Try to sign up again
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity(client: TestClient):
    """Test signup fails for non-existent activity."""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent"
    email = "student@mergington.edu"

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 404 response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_success(client: TestClient):
    """Test successful unregister from an activity."""
    # Arrange: Sign up first
    activity_name = "Gym Class"
    email = "unregister@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: Unregister
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Check success
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]


def test_unregister_missing_student(client: TestClient):
    """Test unregister fails for student not signed up."""
    # Arrange: Use activity and email not signed up
    activity_name = "Art Club"
    email = "notsignedup@mergington.edu"

    # Act: Try to unregister
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Check 404 response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"]


def test_unregister_nonexistent_activity(client: TestClient):
    """Test unregister fails for non-existent activity."""
    # Arrange: Invalid activity
    activity_name = "InvalidActivity"
    email = "student@mergington.edu"

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Check 404
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_root_redirect(client: TestClient):
    """Test GET / redirects to /static/index.html."""
    # Arrange: No setup

    # Act: GET /
    response = client.get("/", follow_redirects=False)

    # Assert: Check redirect
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"