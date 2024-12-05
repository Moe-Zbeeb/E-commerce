API Documentation
==================

This section documents the REST API endpoints for the E-commerce project.

Customer API
------------

.. http:post:: /api/customers/register

    **Description**: Register a new customer.

    **Request Body**:

    - `full_name` (str): Customer's full name.
    - `username` (str): Unique username.
    - `password` (str): Password.
    - `age` (int): Age of the customer.
    - `address` (str): Address of the customer.
    - `gender` (str): Gender.
    - `marital_status` (str): Marital status.

    **Example Request**:

    .. sourcecode:: json

        {
            "full_name": "John Doe",
            "username": "johndoe",
            "password": "securepassword",
            "age": 30,
            "address": "123 Elm St",
            "gender": "Male",
            "marital_status": "Single"
        }

    **Responses**:

    .. http:response:: 201 Created

        {
            "message": "Customer registered successfully"
        }

    .. http:response:: 400 Bad Request

        {
            "error": "Username already exists"
        }

