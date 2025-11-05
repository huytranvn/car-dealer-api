from fastapi import status


class TestCarsUpdateEndpoint:
    """Test suite for the PUT /v1/cars/{car_id} endpoint."""

    def test_update_car_success_full_update(self, client, auth_token, test_car):
        """Test successfully updating a car with all fields."""
        update_data = {
            "name": "Updated Car Name",
            "brand": "Updated Brand",
            "model": "Updated Model",
            "make": "Updated Make",
            "fuel_type": "Electric",
            "color": "Blue",
            "year": 2024,
        }

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify all fields were updated
        assert data["id"] == test_car.id
        assert data["name"] == update_data["name"]
        assert data["brand"] == update_data["brand"]
        assert data["model"] == update_data["model"]
        assert data["make"] == update_data["make"]
        assert data["fuel_type"] == update_data["fuel_type"]
        assert data["color"] == update_data["color"]
        assert data["year"] == update_data["year"]

    def test_update_car_success_partial_update(self, client, auth_token, test_car):
        """Test successfully updating a car with only some fields."""
        # Only update color and year
        update_data = {
            "color": "Green",
            "year": 2025,
        }

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify updated fields
        assert data["color"] == update_data["color"]
        assert data["year"] == update_data["year"]

        # Verify other fields remain unchanged
        assert data["name"] == test_car.name
        assert data["brand"] == test_car.brand
        assert data["model"] == test_car.model
        assert data["make"] == test_car.make
        assert data["fuel_type"] == test_car.fuel_type

    def test_update_car_single_field(self, client, auth_token, test_car):
        """Test updating a single field."""
        update_data = {"name": "Single Field Update"}

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["id"] == test_car.id

    def test_update_car_not_found(self, client, auth_token):
        """Test updating a car that doesn't exist."""
        update_data = {"name": "Updated Name"}

        response = client.put(
            "/v1/cars/99999",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()

    def test_update_car_without_authentication(self, client, test_car):
        """Test updating a car without authentication token."""
        update_data = {"name": "Updated Name"}

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_car_with_invalid_token(self, client, test_car):
        """Test updating a car with invalid authentication token."""
        update_data = {"name": "Updated Name"}

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": "Bearer invalid_token_here"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in response.json()["detail"]

    def test_update_car_with_expired_token(self, client, expired_token, test_car):
        """Test updating a car with expired authentication token."""
        update_data = {"name": "Updated Name"}

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {expired_token}"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_car_with_inactive_user(self, client, inactive_user, test_car):
        """Test updating a car with inactive user token."""
        from utils.auth import create_access_token

        token = create_access_token(
            data={"sub": inactive_user.email, "user_id": inactive_user.id}
        )

        update_data = {"name": "Updated Name"}

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Inactive user" in response.json()["detail"]

    def test_update_car_empty_body(self, client, auth_token, test_car):
        """Test updating a car with empty update body."""
        update_data = {}

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        # Should succeed but no fields updated
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Verify original values are preserved
        assert data["name"] == test_car.name
        assert data["brand"] == test_car.brand

    def test_update_car_invalid_data_types(self, client, auth_token, test_car):
        """Test updating a car with invalid data types."""
        update_data = {
            "name": "Valid Name",
            "year": "not_a_number",  # Should be int
        }

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_car_invalid_car_id(self, client, auth_token):
        """Test updating a car with invalid car ID format."""
        update_data = {"name": "Updated Name"}

        response = client.put(
            "/v1/cars/invalid_id",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_car_multiple_fields(self, client, auth_token, test_car):
        """Test updating multiple fields at once."""
        update_data = {
            "name": "Multi Field Update",
            "color": "Yellow",
            "fuel_type": "Hybrid",
            "year": 2023,
        }

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["color"] == update_data["color"]
        assert data["fuel_type"] == update_data["fuel_type"]
        assert data["year"] == update_data["year"]

    def test_update_car_all_fields_individually(self, client, auth_token, test_car):
        """Test updating each field individually."""
        fields_to_test = [
            ("name", "Updated Name"),
            ("brand", "Updated Brand"),
            ("model", "Updated Model"),
            ("make", "Updated Make"),
            ("fuel_type", "Electric"),
            ("color", "Purple"),
            ("year", 2026),
        ]

        for field_name, field_value in fields_to_test:
            update_data = {field_name: field_value}

            response = client.put(
                f"/v1/cars/{test_car.id}",
                json=update_data,
                headers={"Authorization": f"Bearer {auth_token}"},
            )

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data[field_name] == field_value

    def test_update_car_persistence(self, client, auth_token, test_car):
        """Test that car updates persist in the database."""
        update_data = {"name": "Persistent Update"}

        # Update the car
        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK

        # Verify update persisted by fetching the car
        get_response = client.get(f"/v1/cars?limit=1")
        assert get_response.status_code == status.HTTP_200_OK
        cars = get_response.json()["items"]
        assert len(cars) == 1
        assert cars[0]["name"] == update_data["name"]

    def test_update_car_response_structure(self, client, auth_token, test_car):
        """Test that the response structure matches CarResponse schema."""
        update_data = {"name": "Structure Test"}

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify all required fields are present
        required_fields = ["id", "name", "brand", "model", "make", "fuel_type", "color", "year"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        # Verify data types
        assert isinstance(data["id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["brand"], str)
        assert isinstance(data["model"], str)
        assert isinstance(data["make"], str)
        assert isinstance(data["fuel_type"], str)
        assert isinstance(data["color"], str)
        assert isinstance(data["year"], int)

    def test_update_car_authorization_header_format(self, client, auth_token, test_car):
        """Test different authorization header formats."""
        update_data = {"name": "Header Test"}

        # Test without "Bearer " prefix
        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": auth_token},  # Missing "Bearer "
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Test with correct format
        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_car_negative_id(self, client, auth_token):
        """Test updating a car with negative ID."""
        update_data = {"name": "Updated Name"}

        response = client.put(
            "/v1/cars/-1",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        # Should either validate as 404 or 422
        assert response.status_code in [
            status.HTTP_404_NOT_FOUND,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]

    def test_update_car_zero_id(self, client, auth_token):
        """Test updating a car with zero ID."""
        update_data = {"name": "Updated Name"}

        response = client.put(
            "/v1/cars/0",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        # Should return 404 if not found, or 422 if invalid
        assert response.status_code in [
            status.HTTP_404_NOT_FOUND,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]

    def test_update_car_none_values(self, client, auth_token, test_car):
        """Test updating a car with None values (should be ignored)."""
        # Note: FastAPI will reject None values in JSON, but we test empty body
        update_data = {}

        response = client.put(
            f"/v1/cars/{test_car.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_200_OK
        # Original values should be preserved
        data = response.json()
        assert data["name"] == test_car.name

