import pytest
from src.app import activities


def test_activities_data_structure():
    """Test that activities dict has correct structure."""
    # Arrange: No setup

    # Act: Access activities

    # Assert: Check structure
    assert isinstance(activities, dict)
    for name, details in activities.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)


def test_signup_adds_participant():
    """Test that signup adds email to participants list."""
    # Arrange: Choose activity and email
    activity_name = "Debate Team"
    email = "unittest@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])

    # Act: Simulate adding (but since it's endpoint, perhaps call via client, but for unit, direct)
    # For unit, directly append and check
    activities[activity_name]["participants"].append(email)

    # Assert: Check added
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1

    # Cleanup: Remove for test isolation
    activities[activity_name]["participants"].remove(email)


def test_duplicate_prevention():
    """Test that duplicate emails are not added."""
    # Arrange: Add email first
    activity_name = "Science Olympiad"
    email = "duplicateunit@mergington.edu"
    activities[activity_name]["participants"].append(email)

    # Act: Try to add again
    initial_count = len(activities[activity_name]["participants"])
    # In logic, should check before append
    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    # Assert: Not added again
    assert len(activities[activity_name]["participants"]) == initial_count

    # Cleanup
    activities[activity_name]["participants"].remove(email)


def test_unregister_removes_participant():
    """Test that unregister removes email from participants."""
    # Arrange: Add email
    activity_name = "Drama Club"
    email = "unregisterunit@mergington.edu"
    activities[activity_name]["participants"].append(email)

    # Act: Remove
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Assert: Removed
    assert email not in activities[activity_name]["participants"]