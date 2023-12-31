from tests.test_database import client


def test_register():
    # Test data
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com",
    }

    # Make a POST request to the register endpoint
    response = client.post("/api/v1/auth/register", json=user_data)

    # Assert the response status code is 201
    assert response.status_code == 201

    # Assert the response contains the access token and user ID
    response_data = response.json()
    assert "access_token" in response_data["data"]
    assert "user_id" in response_data["data"]

    # Assert the response message is correct
    assert response_data["message"] == "User registered successfully"
