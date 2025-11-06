import pytest
from fastapi import status


class TestCarsListPublicEndpoint:
    """Test suite for the GET /v1/cars/public endpoint."""

    def test_get_cars_public_no_auth_required(self, client, sample_cars):
        """Test that public endpoint doesn't require authentication."""
        response = client.get("/v1/cars/public")
        assert response.status_code == status.HTTP_200_OK

    def test_get_cars_with_default_params(self, client, sample_cars):
        """Test getting cars with default limit and offset."""
        response = client.get("/v1/cars/public")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 10  # Default limit is 10
        assert data["limit"] == 10
        assert data["offset"] == 0

        # Verify public car structure (limited fields)
        car = data["items"][0]
        assert "id" in car
        assert "name" in car
        assert "brand" in car
        assert "model" in car
        assert "make" in car
        assert "fuel_type" in car
        assert "color" in car
        assert "price" in car
        assert "registered_year" in car
        assert "mileage" in car
        assert "wheel_drive" in car

        # Verify private fields are NOT exposed
        assert "year" not in car
        assert "registered_date" not in car
        assert "registration_number" not in car
        assert "variant" not in car

    def test_get_cars_public_with_pagination(self, client, sample_cars):
        """Test pagination on public endpoint."""
        response = client.get("/v1/cars/public?limit=5&offset=5")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 20
        assert len(data["items"]) == 5
        assert data["limit"] == 5
        assert data["offset"] == 5

    def test_get_cars_public_order_by_price(self, client, sample_cars):
        """Test ordering by price ascending."""
        response = client.get("/v1/cars/public?order_by=price&limit=5")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 5

        # Verify prices are in ascending order
        prices = [float(car["price"]) for car in data["items"]]
        assert prices == sorted(prices)

    def test_get_cars_public_order_by_price_desc(self, client, sample_cars):
        """Test ordering by price descending."""
        response = client.get("/v1/cars/public?order_by=price_desc&limit=5")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 5

        # Verify prices are in descending order
        prices = [float(car["price"]) for car in data["items"]]
        assert prices == sorted(prices, reverse=True)

    def test_get_cars_public_order_by_registered_year(self, client, sample_cars):
        """Test ordering by registered year ascending."""
        response = client.get("/v1/cars/public?order_by=registered_year&limit=5")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 5

        # Verify years are in ascending order
        years = [car["registered_year"] for car in data["items"]]
        assert years == sorted(years)

    def test_get_cars_public_order_by_registered_year_desc(self, client, sample_cars):
        """Test ordering by registered year descending."""
        response = client.get("/v1/cars/public?order_by=registered_year_desc&limit=5")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 5

        # Verify years are in descending order
        years = [car["registered_year"] for car in data["items"]]
        assert years == sorted(years, reverse=True)

    def test_get_cars_public_filter_max_price(self, client, sample_cars):
        """Test filtering by maximum price."""
        max_price = 25000
        response = client.get(f"/v1/cars/public?max_price={max_price}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify all returned cars are within price limit
        for car in data["items"]:
            assert float(car["price"]) <= max_price

    def test_get_cars_public_filter_and_sort(self, client, sample_cars):
        """Test combining filter and sort."""
        max_price = 30000
        response = client.get(f"/v1/cars/public?max_price={max_price}&order_by=price")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify all cars are within price limit
        for car in data["items"]:
            assert float(car["price"]) <= max_price

        # Verify prices are sorted
        prices = [float(car["price"]) for car in data["items"]]
        assert prices == sorted(prices)
