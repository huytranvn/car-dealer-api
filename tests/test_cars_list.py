import pytest
from fastapi import status


class TestCarsListEndpoint:
    """Test suite for the GET /v1/cars endpoint."""

    def test_get_cars_requires_authentication(self, client):
        """Test that endpoint requires authentication."""
        response = client.get("/v1/cars")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_cars_empty_database(self, client, auth_token):
        """Test getting cars when database is empty."""
        response = client.get(
            "/v1/cars",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []
        assert data["limit"] == 10
        assert data["offset"] == 0

    def test_get_cars_with_default_params(self, client, sample_cars, auth_token):
        """Test getting cars with default limit and offset."""
        response = client.get(
            "/v1/cars",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 10  # Default limit is 10
        assert data["limit"] == 10
        assert data["offset"] == 0

        # Verify car structure
        car = data["items"][0]
        assert "id" in car
        assert "name" in car
        assert "brand" in car
        assert "model" in car
        assert "make" in car
        assert "fuel_type" in car
        assert "color" in car
        assert "year" in car

    def test_get_cars_with_custom_limit(self, client, sample_cars, auth_token):
        """Test getting cars with custom limit."""
        response = client.get(
            "/v1/cars?limit=5",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 5
        assert data["limit"] == 5
        assert data["offset"] == 0

    def test_get_cars_with_offset(self, client, sample_cars, auth_token):
        """Test getting cars with offset."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/v1/cars?limit=5&offset=5", headers=headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 5
        assert data["limit"] == 5
        assert data["offset"] == 5

        # Verify we got different cars (checking IDs are different)
        first_page = client.get("/v1/cars?limit=5&offset=0", headers=headers).json()
        assert data["items"][0]["id"] != first_page["items"][0]["id"]

    def test_get_cars_with_max_limit(self, client, sample_cars, auth_token):
        """Test getting cars with maximum allowed limit."""
        response = client.get(
            "/v1/cars?limit=100",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 20  # All cars fit in one page
        assert data["limit"] == 100
        assert data["offset"] == 0

    def test_get_cars_offset_beyond_total(self, client, sample_cars, auth_token):
        """Test getting cars when offset is beyond total count."""
        response = client.get(
            "/v1/cars?limit=10&offset=100",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 0  # No items returned
        assert data["limit"] == 10
        assert data["offset"] == 100

    def test_get_cars_limit_exceeds_total(self, client, sample_cars, auth_token):
        """Test getting cars when limit exceeds total count."""
        response = client.get(
            "/v1/cars?limit=50&offset=0",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 20  # Only returns available items
        assert data["limit"] == 50
        assert data["offset"] == 0

    def test_get_cars_pagination_boundaries(self, client, sample_cars, auth_token):
        """Test pagination at boundaries."""
        # Get last page
        response = client.get(
            "/v1/cars?limit=10&offset=10",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 10
        assert data["limit"] == 10
        assert data["offset"] == 10

    def test_get_cars_invalid_limit_too_small(self, client, sample_cars, auth_token):
        """Test validation for limit too small."""
        response = client.get(
            "/v1/cars?limit=0",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_cars_invalid_limit_too_large(self, client, sample_cars, auth_token):
        """Test validation for limit too large."""
        response = client.get(
            "/v1/cars?limit=101",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_cars_invalid_offset_negative(self, client, sample_cars, auth_token):
        """Test validation for negative offset."""
        response = client.get(
            "/v1/cars?offset=-1",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_cars_car_data_integrity(self, client, sample_cars, auth_token):
        """Test that car data is correctly returned."""
        response = client.get(
            "/v1/cars?limit=1",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        car = data["items"][0]

        # Verify data types
        assert isinstance(car["id"], int)
        assert isinstance(car["name"], str)
        assert isinstance(car["brand"], str)
        assert isinstance(car["model"], str)
        assert isinstance(car["make"], str)
        assert isinstance(car["fuel_type"], str)
        assert isinstance(car["color"], str)
        assert isinstance(car["year"], int)

    def test_get_cars_multiple_pages(self, client, sample_cars, auth_token):
        """Test pagination across multiple pages."""
        headers = {"Authorization": f"Bearer {auth_token}"}
        # Page 1
        page1 = client.get("/v1/cars?limit=5&offset=0", headers=headers).json()
        assert len(page1["items"]) == 5

        # Page 2
        page2 = client.get("/v1/cars?limit=5&offset=5", headers=headers).json()
        assert len(page2["items"]) == 5

        # Page 3
        page3 = client.get("/v1/cars?limit=5&offset=10", headers=headers).json()
        assert len(page3["items"]) == 5

        # Page 4
        page4 = client.get("/v1/cars?limit=5&offset=15", headers=headers).json()
        assert len(page4["items"]) == 5

        # Verify all items are unique across pages
        all_ids = (
            [car["id"] for car in page1["items"]] +
            [car["id"] for car in page2["items"]] +
            [car["id"] for car in page3["items"]] +
            [car["id"] for car in page4["items"]]
        )
        assert len(all_ids) == len(set(all_ids))  # All unique
        assert len(all_ids) == 20  # All cars covered

