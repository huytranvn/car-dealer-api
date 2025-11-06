from fastapi import status


class TestCarsCreateEndpoint:
    """Test suite for the POST /v1/cars endpoint."""

    def test_create_car_success(self, client, auth_token):
        """Test successfully creating a car with valid authentication."""
        car_data = {
            "name": "Toyota Camry",
            "brand": "Toyota",
            "model": "Camry",
            "make": "Toyota Motor Corporation",
            "fuel_type": "Gasoline",
            "color": "Blue",
            "year": 2023,
        }

        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        # Verify response structure
        assert "id" in data
        assert data["name"] == car_data["name"]
        assert data["brand"] == car_data["brand"]
        assert data["model"] == car_data["model"]
        assert data["make"] == car_data["make"]
        assert data["fuel_type"] == car_data["fuel_type"]
        assert data["color"] == car_data["color"]
        assert data["year"] == car_data["year"]

        # Verify car was actually created in database
        get_response = client.get(
            "/v1/cars?limit=1",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert get_response.status_code == status.HTTP_200_OK
        cars = get_response.json()["items"]
        assert len(cars) == 1
        assert cars[0]["id"] == data["id"]

    def test_create_car_without_authentication(self, client):
        """Test creating a car without authentication token."""
        car_data = {
            "name": "Toyota Camry",
            "brand": "Toyota",
            "model": "Camry",
            "make": "Toyota Motor Corporation",
            "fuel_type": "Gasoline",
            "color": "Blue",
            "year": 2023,
        }

        response = client.post("/v1/cars", json=car_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_car_with_invalid_token(self, client):
        """Test creating a car with invalid authentication token."""
        car_data = {
            "name": "Toyota Camry",
            "brand": "Toyota",
            "model": "Camry",
            "make": "Toyota Motor Corporation",
            "fuel_type": "Gasoline",
            "color": "Blue",
            "year": 2023,
        }

        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": "Bearer invalid_token_here"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in response.json()["detail"]

    def test_create_car_with_expired_token(self, client, expired_token):
        """Test creating a car with expired authentication token."""
        car_data = {
            "name": "Toyota Camry",
            "brand": "Toyota",
            "model": "Camry",
            "make": "Toyota Motor Corporation",
            "fuel_type": "Gasoline",
            "color": "Blue",
            "year": 2023,
        }

        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": f"Bearer {expired_token}"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_car_with_inactive_user(self, client, inactive_user):
        """Test creating a car with inactive user token."""
        from utils.auth import create_access_token

        token = create_access_token(
            data={"sub": inactive_user.email, "user_id": inactive_user.id}
        )

        car_data = {
            "name": "Toyota Camry",
            "brand": "Toyota",
            "model": "Camry",
            "make": "Toyota Motor Corporation",
            "fuel_type": "Gasoline",
            "color": "Blue",
            "year": 2023,
        }

        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Inactive user" in response.json()["detail"]

    def test_create_car_missing_required_fields(self, client, auth_token):
        """Test creating a car with missing required fields."""
        car_data = {
            "name": "Toyota Camry",
            # Missing brand, model, make, fuel_type, color, year
        }

        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_car_invalid_data_types(self, client, auth_token):
        """Test creating a car with invalid data types."""
        car_data = {
            "name": "Toyota Camry",
            "brand": "Toyota",
            "model": "Camry",
            "make": "Toyota Motor Corporation",
            "fuel_type": "Gasoline",
            "color": "Blue",
            "year": "not_a_number",  # Should be int
        }

        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_car_empty_strings(self, client, auth_token):
        """Test creating a car with empty string values."""
        car_data = {
            "name": "",
            "brand": "",
            "model": "",
            "make": "",
            "fuel_type": "",
            "color": "",
            "year": 2023,
        }

        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        # Should still create (empty strings are valid, database constraints would handle)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_422_UNPROCESSABLE_ENTITY]

    def test_create_multiple_cars(self, client, auth_token):
        """Test creating multiple cars."""
        car_data_1 = {
            "name": "Toyota Camry",
            "brand": "Toyota",
            "model": "Camry",
            "make": "Toyota Motor Corporation",
            "fuel_type": "Gasoline",
            "color": "Blue",
            "year": 2023,
        }

        car_data_2 = {
            "name": "Honda Accord",
            "brand": "Honda",
            "model": "Accord",
            "make": "Honda Motor Company",
            "fuel_type": "Hybrid",
            "color": "Red",
            "year": 2024,
        }

        # Create first car
        response1 = client.post(
            "/v1/cars",
            json=car_data_1,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response1.status_code == status.HTTP_201_CREATED
        car1_id = response1.json()["id"]

        # Create second car
        response2 = client.post(
            "/v1/cars",
            json=car_data_2,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response2.status_code == status.HTTP_201_CREATED
        car2_id = response2.json()["id"]

        # Verify both cars were created with different IDs
        assert car1_id != car2_id

        # Verify both cars exist in the database
        get_response = client.get(
            "/v1/cars?limit=10",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert get_response.status_code == status.HTTP_200_OK
        cars = get_response.json()["items"]
        car_ids = [car["id"] for car in cars]
        assert car1_id in car_ids
        assert car2_id in car_ids

    def test_create_car_all_fuel_types(self, client, auth_token):
        """Test creating cars with different fuel types."""
        fuel_types = ["Gasoline", "Diesel", "Electric", "Hybrid", "Plug-in Hybrid"]

        for fuel_type in fuel_types:
            car_data = {
                "name": f"Test Car {fuel_type}",
                "brand": "Test Brand",
                "model": "Test Model",
                "make": "Test Make",
                "fuel_type": fuel_type,
                "color": "White",
                "year": 2023,
            }

            response = client.post(
                "/v1/cars",
                json=car_data,
                headers={"Authorization": f"Bearer {auth_token}"},
            )

            assert response.status_code == status.HTTP_201_CREATED
            assert response.json()["fuel_type"] == fuel_type

    def test_create_car_response_structure(self, client, auth_token):
        """Test that the response structure matches CarResponse schema."""
        car_data = {
            "name": "Tesla Model 3",
            "brand": "Tesla",
            "model": "Model 3",
            "make": "Tesla Inc",
            "fuel_type": "Electric",
            "color": "Black",
            "year": 2023,
        }

        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == status.HTTP_201_CREATED
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

    def test_create_car_authorization_header_format(self, client, auth_token):
        """Test different authorization header formats."""
        car_data = {
            "name": "Test Car",
            "brand": "Test Brand",
            "model": "Test Model",
            "make": "Test Make",
            "fuel_type": "Gasoline",
            "color": "Blue",
            "year": 2023,
        }

        # Test without "Bearer " prefix
        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": auth_token},  # Missing "Bearer "
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Test with correct format
        response = client.post(
            "/v1/cars",
            json=car_data,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_201_CREATED

