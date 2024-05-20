from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine
import models
import schemas
import crud
from auth import create_access_token, verify_password, decode_access_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI(debug=True, docs_url="/")


# Dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, description="Register a new user.")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    This endpoint allows users to register by providing their username and password.

    Parameters:
        - user: The user details to be registered, including username and password.
          This data is received as per the UserCreate schema defined in schemas.py.
        - db (Session): The database session dependency obtained using the get_db function.
          It provides access to the database to perform CRUD operations.

    Returns:
        - User: Returns the newly created user details upon successful registration,
          excluding sensitive information like the password.

    Raises:
        - HTTPException: Raises a 400 error if the username is already registered.
    """


@app.post(
    "/token",
    response_model=dict,
    description="Obtain an access token for authentication.",
)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    This endpoint allows users to obtain an access token by providing their username and password.
    The access token is used for subsequent authenticated requests.

    Parameters:
        - db (Session): The database session dependency obtained using the get_db function.
          It provides access to the database to perform CRUD operations.
        - form_data (OAuth2PasswordRequestForm): The form data containing the username and password
          for authentication.

    Returns:
        - dict: Returns a dictionary containing the access token and its type upon successful authentication.

    Raises:
        - HTTPException: Raises a 401 error if the provided username or password is incorrect.
    """


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    This dependency function retrieves the current user based on the provided access token.

    Parameters:
        - db (Session): The database session dependency obtained using the get_db function.
          It provides access to the database to perform CRUD operations.
        - token (str): The access token obtained from the request header.

    Returns:
        - User: Returns the current user based on the access token.

    Raises:
        - HTTPException: Raises a 401 error if the access token is invalid or the user is not found.
    """


@app.get(
    "/products",
    response_model=List[schemas.Product],
    description="Retrieve a list of products.",
)
def read_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    This endpoint retrieves a list of products from the database.

    Parameters:
        - skip (int): The number of products to skip (for pagination).
        - limit (int): The maximum number of products to retrieve (for pagination).
        - db (Session): The database session dependency obtained using the get_db function.
          It provides access to the database to perform CRUD operations.
        - current_user (User): The current authenticated user.

    Returns:
        - List[Product]: Returns a list of products based on the provided skip and limit parameters.
    """


@app.post(
    "/products", response_model=schemas.Product, description="Create a new product."
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    This endpoint creates a new product in the database.

    Parameters:
        - product (ProductCreate): The product details to be created, including title, description, and price.
        - db (Session): The database session dependency obtained using the get_db function.
          It provides access to the database to perform CRUD operations.
        - current_user (User): The current authenticated user.

    Returns:
        - Product: Returns the newly created product details upon successful creation.
    """


@app.get(
    "/products/{product_id}",
    response_model=schemas.Product,
    description="Retrieve details of a specific product.",
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    This endpoint retrieves details of a specific product based on its ID.

    Parameters:
        - product_id (int): The ID of the product to retrieve.
        - db (Session): The database session dependency obtained using the get_db function.
          It provides access to the database to perform CRUD operations.
        - current_user (User): The current authenticated user.

    Returns:
        - Product: Returns the details of the specified product.

    Raises:
        - HTTPException: Raises a 404 error if the specified product ID is not found.
    """


@app.put(
    "/products/{product_id}",
    response_model=schemas.Product,
    description="Update an existing product.",
)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    This endpoint updates an existing product based on its ID.

    Parameters:
        - product_id (int): The ID of the product to update.
        - product (ProductCreate): The updated product details, including title, description, and price.
        - db (Session): The database session dependency obtained using the get_db function.
          It provides access to the database to perform CRUD operations.
        - current_user (User): The current authenticated user.

    Returns:
        - Product: Returns the updated product details upon successful update.

    Raises:
        - HTTPException: Raises a 404 error if the specified product ID is not found.
    """


@app.delete(
    "/products/{product_id}",
    response_model=dict,
    description="Delete a product by its ID.",
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    This endpoint deletes a product based on its ID.

    Parameters:
        - product_id (int): The ID of the product to delete.
        - db (Session): The database session dependency obtained using the get_db function.
          It provides access to the database to perform CRUD operations.
        - current_user (User): The current authenticated user.

    Returns:
        - dict: Returns a dictionary confirming the deletion of the product.
    """
