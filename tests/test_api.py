import pytest
import requests

BASE_URL = "http://localhost:8000"


@pytest.fixture
def create_product():
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "quantity": 100,
    }
    response = requests.post(f"{BASE_URL}/products/", json=product_data)
    return response.json()


def test_read_product(create_product):
    product_id = create_product["id"]
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == product_id
    assert product["name"] == create_product["name"]
    assert product["description"] == create_product["description"]
    assert product["price"] == create_product["price"]
    assert product["quantity"] == create_product["quantity"]


def test_update_product(create_product):
    product_id = create_product["id"]
    updated_data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 20.0,
        "quantity": 200,
    }
    response = requests.put(
        f"{BASE_URL}/products/{product_id}", json=updated_data
    )
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == product_id
    assert product["name"] == updated_data["name"]
    assert product["description"] == updated_data["description"]
    assert product["price"] == updated_data["price"]
    assert product["quantity"] == updated_data["quantity"]


def test_delete_product(create_product):
    product_id = create_product["id"]
    response = requests.delete(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == product_id

    response = requests.get(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 404


def test_create_order(create_product):
    product_id = create_product["id"]
    order_data = {"items": [{"product_id": product_id, "quantity": 5}]}
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    assert response.status_code == 200
    order = response.json()
    assert order["status"] == "в процессе"
    assert len(order["items"]) == 1
    assert order["items"][0]["product_id"] == product_id
    assert order["items"][0]["quantity"] == 5
