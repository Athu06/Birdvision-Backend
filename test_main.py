from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import models

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:atharva@localhost/Birdvision"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_user():
    response = client.post(
        "/users/", json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_login():
    client.post("/users/", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_product():
    client.post("/users/", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/products",
        headers=headers,
        json={
            "title": "Test Product",
            "description": "This is a test product",
            "price": 9.99,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Product"


def test_read_products():
    client.post("/users/", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post(
        "/products",
        headers=headers,
        json={
            "title": "Test Product 1",
            "description": "This is a test product",
            "price": 9.99,
        },
    )
    client.post(
        "/products",
        headers=headers,
        json={
            "title": "Test Product 2",
            "description": "This is another test product",
            "price": 19.99,
        },
    )
    response = client.get("/products?skip=0&limit=1", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_product():
    client.post("/users/", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/products",
        headers=headers,
        json={
            "title": "Test Product",
            "description": "This is a test product",
            "price": 9.99,
        },
    )
    product_id = response.json()["id"]
    update_data = {
        "title": "Updated Product",
        "description": "This is an updated test product",
        "price": 10.99,
    }
    response = client.put(f"/products/{product_id}", headers=headers, json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Product"


def test_delete_product():
    client.post("/users/", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/products",
        headers=headers,
        json={
            "title": "Test Product",
            "description": "This is a test product",
            "price": 9.99,
        },
    )
    product_id = response.json()["id"]
    response = client.delete(f"/products/{product_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"detail": "Product deleted"}


def test_read_product_not_found():
    client.post("/users/", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        "/products/999", headers=headers
    )  # Assuming product with ID 999 does not exist
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_read_products_pagination():
    client.post("/users/", json={"username": "testuser", "password": "testpass"})
    response = client.post(
        "/token", data={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    client.post(
        "/products",
        headers=headers,
        json={
            "title": "Test Product 1",
            "description": "This is a test product",
            "price": 9.99,
        },
    )
    client.post(
        "/products",
        headers=headers,
        json={
            "title": "Test Product 2",
            "description": "This is another test product",
            "price": 19.99,
        },
    )
    client.post(
        "/products",
        headers=headers,
        json={
            "title": "Test Product 3",
            "description": "This is yet another test product",
            "price": 29.99,
        },
    )
    response = client.get("/products?skip=1&limit=2", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


Base.metadata.drop_all(bind=engine)
