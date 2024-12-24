# API Documentation for Menu Management System

This API provides functionalities for managing users, menu items, cart items, and orders. It supports role-based access control with three primary roles: **Manager**, **Delivery Crew**, and **Customer**. The API enforces authentication, authorization, and proper HTTP status code responses.

---

## HTTP Status Codes

| Status Code          | Description                                        |
| -------------------- | -------------------------------------------------- |
| **200 OK**           | Successful GET, PUT, PATCH, or DELETE operations.  |
| **201 Created**      | Successful POST operations.                        |
| **401 Unauthorized** | Authentication failure due to invalid credentials. |
| **403 Forbidden**    | Authorization failure for restricted actions.      |
| **400 Bad Request**  | Validation failures for invalid input data.        |
| **404 Not Found**    | Resource not found for the requested operation.    |

---

## User Registration and Authentication

### Endpoints

- **`POST /api/users`**

  - **Role**: No role required
  - **Purpose**: Registers a new user with `name`, `email`, and `password`.
  - **Responses**:
    - **201 Created**: User successfully registered.
    - **400 Bad Request**: Validation error for missing or invalid data.

- **`GET /api/users/me/`**

  - **Role**: Authenticated users
  - **Purpose**: Fetches details of the currently authenticated user.
  - **Responses**:
    - **200 OK**: User details retrieved.
    - **401 Unauthorized**: Authentication failure.

- **`POST /token/login/`**
  - **Role**: Valid username and password
  - **Purpose**: Generates an access token for API access.
  - **Responses**:
    - **200 OK**: Token generated successfully.
    - **401 Unauthorized**: Invalid credentials.

---

## Menu Items Management

### Customer/Delivery Crew Access

- **`GET /api/menu-items`**
  - **Purpose**: Lists all menu items.
  - **Responses**:
    - **200 OK**: List of menu items.
- **`POST, PUT, PATCH, DELETE /api/menu-items`**

  - **Purpose**: Access denied for these roles.
  - **Responses**:
    - **403 Forbidden**: Unauthorized access.

- **`GET /api/menu-items/{menuItem}`**
  - **Purpose**: Fetches details of a specific menu item.
  - **Responses**:
    - **200 OK**: Menu item details retrieved.
    - **404 Not Found**: Menu item does not exist.

### Manager Access

- **`POST /api/menu-items`**

  - **Purpose**: Adds a new menu item.
  - **Responses**:
    - **201 Created**: Menu item created successfully.

- **`PUT, PATCH /api/menu-items/{menuItem}`**

  - **Purpose**: Updates an existing menu item.
  - **Responses**:
    - **200 OK**: Menu item updated successfully.

- **`DELETE /api/menu-items/{menuItem}`**
  - **Purpose**: Deletes an existing menu item.
  - **Responses**:
    - **200 OK**: Menu item deleted.
    - **404 Not Found**: Menu item does not exist.

---

## User Group Management

### Manager Access

- **`GET /api/groups/manager/users`**

  - **Purpose**: Retrieves a list of all managers.
  - **Responses**:
    - **200 OK**: List of managers.

- **`POST /api/groups/manager/users`**

  - **Purpose**: Adds a user to the manager group.
  - **Responses**:
    - **201 Created**: User added to the manager group.

- **`DELETE /api/groups/manager/users/{userId}`**
  - **Purpose**: Removes a user from the manager group.
  - **Responses**:
    - **200 OK**: User removed successfully.
    - **404 Not Found**: User does not exist.

---

## Cart Management

### Customer Access

- **`GET /api/cart/menu-items`**

  - **Purpose**: Retrieves current cart items for the authenticated user.
  - **Responses**:
    - **200 OK**: Cart items retrieved.

- **`POST /api/cart/menu-items`**

  - **Purpose**: Adds a menu item to the cart.
  - **Responses**:
    - **201 Created**: Item added to the cart.

- **`DELETE /api/cart/menu-items`**
  - **Purpose**: Clears all cart items for the authenticated user.
  - **Responses**:
    - **200 OK**: Cart items cleared.

---

## Order Management

### Customer Access

- **`GET /api/orders`**

  - **Purpose**: Retrieves all orders for the authenticated user.
  - **Responses**:
    - **200 OK**: Orders retrieved.

- **`POST /api/orders`**

  - **Purpose**: Creates a new order from cart items.
  - **Responses**:
    - **201 Created**: Order created.

- **`GET /api/orders/{orderId}`**
  - **Purpose**: Retrieves details of a specific order.
  - **Responses**:
    - **200 OK**: Order details retrieved.
    - **404 Not Found**: Order does not exist.

### Manager Access

- **`GET /api/orders`**

  - **Purpose**: Lists all orders across all users.
  - **Responses**:
    - **200 OK**: Orders retrieved.

- **`PUT, PATCH /api/orders/{orderId}`**

  - **Purpose**: Updates order status or assigns a delivery crew.
  - **Responses**:
    - **200 OK**: Order updated.

- **`DELETE /api/orders/{orderId}`**
  - **Purpose**: Deletes an order.
  - **Responses**:
    - **200 OK**: Order deleted.

### Delivery Crew Access

- **`GET /api/orders`**

  - **Purpose**: Lists all orders assigned to the delivery crew.
  - **Responses**:
    - **200 OK**: Orders retrieved.

- **`PATCH /api/orders/{orderId}`**
  - **Purpose**: Updates the status of an assigned order.
  - **Responses**:
    - **200 OK**: Order status updated.
    - **403 Forbidden**: Unauthorized changes.

---

## Additional Features

### Filtering, Pagination, and Sorting

- Supported for `/api/menu-items` and `/api/orders` endpoints.
- Allows dynamic filtering and ordering of results.

### Throttling

- Configured throttling for both authenticated and unauthenticated users to prevent abuse.
