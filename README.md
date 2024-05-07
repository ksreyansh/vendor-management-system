# Vendor Management System

(This project is done as an assignment given by the Fatmug)

Vendor Management System is a platform that companies can use to manage its external workforce. For businesses, Vendor stands for an external supplier of goods and/or services. This project is a simple implementation of a vendor management system using Django Rest Framework with the database being SQLite3

## Models
This system employs following four models:

#### 1. Vendor Model
This model stores essential information about each vendor and their performancemetrics.

Fields:
- name: CharField - Vendor's name.
- contact_details: TextField - Contact information of the vendor.
- address: TextField - Physical address of the vendor.
- vendor_code: CharField - A unique identifier for the vendor.
- on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
- quality_rating_avg: FloatField - Average rating of quality based on purchase
orders.
- average_response_time: FloatField - Average time taken to acknowledge
purchase orders.
- fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.

#### 2. Purchase Order (PO) Model
This model captures the details of each purchase order and is used to calculate various performance metrics.

Fields:

- po_number: CharField - Unique number identifying the PO.
- vendor: ForeignKey - Link to the Vendor model.
- order_date: DateTimeField - Date when the order was placed.
- delivery_date: DateTimeField - Expected or actual delivery date of the order.
- items: JSONField - Details of items ordered.
- quantity: IntegerField - Total quantity of items in the PO.
- status: CharField - Current status of the PO (e.g., pending, completed, canceled).
- quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
- issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
- acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor
- acknowledged the PO.
- completion_date: DateTimeField - Timestamp when the vendor completed the order

#### 3. Historical Performance Model
This model optionally stores historical data on vendor performance, enabling trend analysis.

Fields:
- vendor: ForeignKey - Link to the Vendor model.
- date: DateTimeField - Date of the performance record.
- on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
- quality_rating_avg: FloatField - Historical record of the quality rating average.
- average_response_time: FloatField - Historical record of the average response
time.
- fulfillment_rate: FloatField - Historical record of the fulfilment rate.

#### 4. Custom User Model
This model is for customizing management of users in the system.

Fields:
- email: EmailField - Email of the user
- password: Predefined password field

## Setup Instructions

### Step 1: Clone the Repository
- Open your terminal or command prompt.
- Navigate to the directory where you want to clone the repository.
- Run the following command to clone the repository:
```
git clone https://github.com/ksreyansh/vendor-management-system.git
```
- This will create a local copy of the repository on your machine.

### Step 2: Navigate to the Project Directory
- After cloning the repository, navigate into the project directory by running:
```
cd vendor-management-system
```

### Step 3: Set Up Virtual Environment (Optional but Recommended)
- It's recommended to use a virtual environment to manage dependencies for your Django project.
- Create a virtual environment by running:
```
python -m venv venv
```
##### Activate the virtual environment:
- On Windows:
```
venv\Scripts\activate
```
- On macOS and Linux:
```
source venv/bin/activate
```

### Step 4: Install Dependencies
- With the virtual environment activated, install the project dependencies using pip:
```
pip install -r requirements.txt
```

### Step 5: Set Up Database
- Configure Database: Open the settings.py file inside the vendor_management_system directory.
- In the DATABASES section, configure your database settings according to your preference. By default, Django uses SQLite for local development.

### Step 6: Apply Migrations
- Run the following command to apply migrations and set up the initial database schema:
```
python manage.py migrate
```

### Step 7: Create a Superuser (Optional)
- If you want to access the Django admin interface, create a superuser account by running:
```
python manage.py createsuperuser
```
- Follow the prompts to enter a email, and password for the superuser.

### Step 8: Run Development Server
- Start the development server by running:
```
python manage.py runserver
```
- This will start the development server, and you can access the Django project in a web browser at http://127.0.0.1:8000/.

## API Reference

The following are the details of all the API endpoints along with their usage description.

### AuthenticationAPI

#### Login
Login into the system

```
POST /auth/login/
```
Data parameters:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`      | `string` | Registered email |
| `password`      | `string` | Registered password |

#### Logout
Logs out the user

```
POST /auth/logout/
```

### VendorAPI

#### Get all vendors
Gets details of all the vendors in the database

```
  GET /api/vendor/
```

#### Get individual vendor
Fetches details of individual vendor by its unique identifier

```
  GET /api/vendor/{vendor_code}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `vendor_code`      | `string` | Unique identifier of the vendor | 


#### Create vendor profile
Creates a new vendor profile with initial values being 0.0 for all the metrics

```
  POST /api/vendor/
```

#### Update vendor profile
Updates details of the vendor by its unique identifier

```
  PUT /api/vendor/{vendor_code}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `vendor_code` | `string` | Unique identifier of the vendor |


#### Delete vendor profile
Deletes a vendor profile

```
  DELETE /api/vendor/{vendor_code}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `vendor_code` | `string` | Unique identifier of the vendor |



### PurchaseOrderAPI

#### Get all purchase orders
Fetches details of all the purchase orders in the database

```
  GET /api/purchase_orders/
```

#### Get individual purchase order
Fetches details of a individual purchase order by its unique identifier

```
  GET /api/purchase_orders/{po_number}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `po_number`      | `string` | Unique identifier of the purchase order |


#### Create purchase order
Creates a new purchase order

```
  POST /api/purchase_orders/
```

#### Update purchase order
Updates details of the order by its unique identifier

```
  PUT /api/purchase_orders/{po_number}
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_number` | `string` | Unique identifier of the purchase order |

#### Delete purchase order
Deletes a purchase order

```
  DELETE /api/purchase_orders/{po_number}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_number` | `string` | Unique identifier of the purchase order |

#### Acknowledge purchase order

This API endpoint is to simulate a vendor acknowledging a purchase order. This would trigger a signal in the backend which would calculate the average response time (performance metrics) of the vendor for historical performance of the vendor.

The signal also simulataneously updates the metrics in Vendor model.

```
    PATCH performance/{po_number}/acknowledge/
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `po_number` | `string` | Unique identifier of the purchase order |



### HistoricalPerformanceAPI
Fetches performance metrics for a vendor by unique identifier of the vendor

```
    GET /api/vendor/{vendor_code}/performance/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `vendor_code` | `string` | Fetches performance metrics for a vendor by unique identifier of the vendor |


# Testing Suite

The test suite for this package comes with the following tests

## Instruction for running tests

- Navigate to the directory containing the Django project (vendor_management_system).
- Run the following command to execute the test suite:
```
python manage.py test
```
Successful completion returns a message of the format "Test: TestName -> Completed" in the command prompt


## Description of test cases

The following is a brief description of the test cases defined for this application.

## AuthenticationAPI tests

The authentication module consists of a custom user model (CustomUserModel) with a separate model manager for it

### User Management Testing
#### UserManagerTests

####  `test_create_user()`
    Purpose: Test the creation of a normal user.

- Steps:
    1. Create a user with a specified email and password.
    2. Assert that the user's email matches the specified email.
    3. Assert that the user is active, not a staff member, and not a superuser.
    4. Assert that the user does not have a username.
    5. Test various error cases:
    - Attempt to create a user without any arguments.
    - Attempt to create a user with an empty email.
    - Attempt to create a user with an empty email and password.

#### `test_create_superuser()`

    Purpose: Test the creation of a superuser.

- Steps:
    1. Create a superuser with a specified email and password.
    2. Assert that the superuser's email matches the specified email.
    3. Assert that the superuser is active, a staff member, and a superuser.
    4. Assert that the superuser does not have a username.
    5. Test an error case:
    - Attempt to create a superuser with an invalid is_superuser flag.

### AuthenticateAPITestCase
#### `setUp()`
    Purpose: Set up the necessary objects for API authentication testing.

- Steps:
    1. Create a custom user with a specified email and password.
    2. Generate an authentication token for the user.

#### `test_login_success()`

    Purpose: Test successful user login via API.

- Steps:
    1. Send a POST request to the login endpoint with valid credentials.
    2. Assert that the response status code is HTTP 200 OK.
    3. Assert that the response contains a token.

#### `test_login_failure_invalid_credentials()`

    Purpose: Test user login failure due to invalid credentials via API.

- Steps:
    1. Send a POST request to the login endpoint with invalid credentials.
    2. Assert that the response status code is HTTP 401 UNAUTHORIZED.
    3. Assert that the response contains an error message.

#### `test_login_failure_missing_credentials()`

    Purpose: Test user login failure due to missing credentials via API.

- Steps:
    1. Send a POST request to the login endpoint without specifying the password.
    2. Assert that the response status code is HTTP 400 BAD REQUEST.

#### `test_login_failure_invalid_method()`

    Purpose: Test user login failure due to using an invalid HTTP method via API.

- Steps:
    1. Send a GET request to the login endpoint.
    2. Assert that the response status code is HTTP 405 METHOD NOT ALLOWED.

#### UserLogoutViewTestCase
#### `setUp()`

    Purpose: Set up the necessary objects for testing user logout via API.

- Steps:
    1. Create a superuser with a specified email and password.
    2. Generate an authentication token for the superuser.
    3. Set up an API client and force authentication with the superuser.

#### `test_logout_success()`

    Purpose: Test successful user logout via API.

- Steps:
    1. Send a POST request to the logout endpoint with a valid token.
    2. Assert that the response status code is HTTP 200 OK.
    3. Assert that the response contains a success message.

##### `test_logout_failure_invalid_token()`

    Purpose: Test user logout failure due to using an invalid token via API.

- Steps:
    1. Send a POST request to the logout endpoint with an invalid token.
    2. Assert that the response status code is HTTP 401 UNAUTHORIZED.
    3. Assert that the response contains an error message.


### Vendor API Testing

#### VendorTestCaseGet
#### `setUp()`

    Purpose: Set up necessary objects and data for testing GET requests related to vendors.

- Steps:
    1. Create a superuser for testing.
    2. Authenticate the test client with the superuser.
    3. Generate an authentication token for the superuser.
    4. Create ten sample vendor objects using Faker library for generating fake data.

#### `test_get_all_vendors()`

    Purpose: Test retrieving details of all vendors.

- Steps:
    1. Send a GET request to the endpoint for retrieving all vendors.
    2. Assert that the response status code is HTTP 200 OK.
    3. Assert that the number of retrieved vendors matches the expected count.

#### `test_get_vendor_by_id()`
    
    Purpose: Test retrieving details of a specific vendor by its ID.

- Steps:
    1. Send a GET request to the endpoint for retrieving a vendor by its ID.
    2. Assert that the response status code is HTTP 200 OK.

#### `test_get_nonexistent_vendor()`
    
    Purpose: Test retrieving details of a vendor with a non-existent ID.

- Steps:
    1. Send a GET request to the endpoint for retrieving a vendor with a non-existent ID.
    2. Assert that the response status code is HTTP 404 NOT FOUND.

#### VendorTestCasePost

#### `setUp()`

    Purpose: Set up necessary objects and data for testing POST requests related to vendors.

- Steps: Same as in VendorTestCaseGet.setUp().

#### `test_create_vendor()`

    Purpose: Test creating a new vendor.

- Steps:
    1. Send a POST request to the endpoint for creating a vendor with valid data.
    2. Assert that the response status code is HTTP 201 CREATED.
    3. Assert that the created vendor's details match the provided data.

#### `test_invalid_create_vendor()`
    Purpose: Test creating a new vendor with invalid data.
- Steps:
    1. Send a POST request to the endpoint for creating a vendor with invalid data.
    2. Assert that the response status code is HTTP 400 BAD REQUEST.

#### VendorTestCasePut
#### `setUp()`
    
    Purpose: Set up necessary objects and data for testing PUT requests related to vendors.

- Steps: Same as in VendorTestCaseGet.setUp().

#### `test_valid_put()`

    Purpose: Test updating vendor details with valid data.

- Steps:
    1. Send a PUT request to the endpoint for updating a vendor's details with valid data.
    2. Assert that the response status code is HTTP 200 OK.
    3. Assert that the vendor's details have been updated as expected.

#### `test_invalid_put()`
    Purpose: Test updating vendor details with invalid data.
- Steps:
    1. Send a PUT request to the endpoint for updating a vendor's details with invalid data.
    2. Assert that the response status code is HTTP 400 BAD REQUEST.

#### VendorTestCaseDelete
#### `setUp()`
    Purpose: Set up necessary objects and data for testing DELETE requests related to vendors.
- Steps: Same as in VendorTestCaseGet.setUp().

#### `test_valid_delete()`
    Purpose: Test deleting a vendor.
- Steps:
    1. Send a DELETE request to the endpoint for deleting a vendor.
    2. Assert that the response status code is HTTP 204 NO CONTENT.
    3. Assert that the vendor has been deleted from the database.

#### `test_invalid_delete()`
    Purpose: Test attempting to delete a non-existent vendor.
- Steps:
    1. Send a DELETE request to the endpoint for deleting a non-existent vendor.
    2. Assert that the response status code is HTTP 404 NOT FOUND.

### Purchase Order (PO) API Testing

#### POTestCaseSetUpGet

#### `setUp()`

    Purpose: Set up necessary objects and data for testing GET requests related to purchase orders.
- Steps:
    1. Create a superuser for testing.
    2. Authenticate the test client with the superuser.
    3. Generate an authentication token for the superuser.
    4. Create a vendor object for testing.
    5. Create ten sample purchase order objects using Faker library for generating fake data.

#### POTestCases
#### `test_get_all_orders()`
    Purpose: Test retrieving details of all purchase orders.
- Steps:
    1. Send a GET request to the endpoint for retrieving all purchase orders.
    2. Assert that the response status code is HTTP 200 OK.
    3. Assert that the number of retrieved purchase orders matches the expected count.

#### `test_get_order_by_id()`
    Purpose: Test retrieving details of a specific purchase order by its ID.
- Steps:
    1. Send a GET request to the endpoint for retrieving a purchase order by its ID.
    2. Assert that the response status code is HTTP 200 OK.

#### `test_get_nonexistent_order()`
    Purpose: Test retrieving details of a purchase order with a non-existent ID.
- Steps:
    1. Send a GET request to the endpoint for retrieving a purchase order with a non-existent ID.
    2. Assert that the response status code is HTTP 404 NOT FOUND.

#### POTestCasePost
#### `setUp()`

    Purpose: Set up necessary objects and data for testing POST requests related to purchase orders.
- Steps: Same as in POTestCaseSetUpGet.setUp().

#### `test_create_order()`

    Purpose: Test creating a new purchase order.
- Steps:
    1. Send a POST request to the endpoint for creating a purchase order with valid data.
    2. Assert that the response status code is HTTP 201 CREATED.
    3. Assert that the created purchase order's details match the provided data.

#### `test_invalid_create_order()`

    Purpose: Test creating a new purchase order with invalid data.
- Steps:
    1. Send a POST request to the endpoint for creating a purchase order with invalid data.
    2. Assert that the response status code is HTTP 400 BAD REQUEST.

#### POTestCasePut
#### `setUp()`
    Purpose: Set up necessary objects and data for testing PUT requests related to purchase orders.
- Steps: Same as in POTestCaseSetUpGet.setUp().

#### `test_valid_put()`
    Purpose: Test updating purchase order details with valid data.
- Steps:
    1. Send a PUT request to the endpoint for updating a purchase order's details with valid data.
    2. Assert that the response status code is HTTP 200 OK.
    3. Assert that the purchase order's details have been updated as expected.

#### `test_invalid_put()`
    Purpose: Test updating purchase order details with invalid data.
- Steps:
    1. Send a PUT request to the endpoint for updating a purchase order's details with invalid data.
    2. Assert that the response status code is HTTP 400 BAD REQUEST.

#### POTestCaseDelete
#### `setUp()`
    Purpose: Set up necessary objects and data for testing DELETE requests related to purchase orders.
- Steps: Same as in POTestCaseSetUpGet.setUp().

#### `test_valid_delete()`

    Purpose: Test deleting a purchase order.

-Steps:
    1. Send a DELETE request to the endpoint for deleting a purchase order.
    2. Assert that the response status code is HTTP 204 NO CONTENT.
    3. Assert that the purchase order has been deleted from the database.

#### `test_invalid_delete()`
    Purpose: Test attempting to delete a non-existent purchase order.
- Steps:
    1. Send a DELETE request to the endpoint for deleting a non-existent purchase order.
    2. Assert that the response status code is HTTP 404 NOT FOUND.

### Acknowledge Purchase Order API Testing
#### AcknowledgePOTestCase
#### `setUp()`
    Purpose: Set up necessary objects and data for testing the acknowledgment of purchase orders.
- Steps:
    1. Create a superuser for testing.
    2. Authenticate the test client with the superuser.
    3. Generate an authentication token for the superuser.
    4. Create a vendor object for testing.
    5. Create a sample purchase order object for testing acknowledgment.

#### `test_acknowledge_valid_po_number()`
    Purpose: Test acknowledging a purchase order with a valid PO number.
- Steps:
    1. Send a PATCH request to the endpoint for acknowledging the purchase order.
    2. Assert that the response status code is HTTP 200 OK.
    3. Refresh the purchase order object from the database and assert that the 
acknowledgment date is not None.

#### `test_acknowledge_invalid_po_number()`
    Purpose: Test acknowledging a purchase order with an invalid PO number.
- Steps:
    1. Send a PATCH request to the endpoint for acknowledging a purchase order with  an invalid PO number.
    2. Assert that the response status code is HTTP 404 NOT FOUND.

### Acknowledge Purchase Order API Testing
#### AcknowledgePOTestCase
#### `setUp()`
    Purpose: Set up necessary objects and data for testing the acknowledgment of purchase orders.
- Steps:
    1. Create a superuser for testing.
    2. Authenticate the test client with the superuser.
    3. Generate an authentication token for the superuser.
    4. Create a vendor object for testing.
    5. Create a sample purchase order object for testing acknowledgment.

#### `test_acknowledge_valid_po_number()`
    Purpose: Test acknowledging a purchase order with a valid PO number.
- Steps:
    1. Send a PATCH request to the endpoint for acknowledging the purchase order.
    2. Assert that the response status code is HTTP 200 OK.
    3. Refresh the purchase order object from the database and assert that the acknowledgment date is not None.

#### `test_acknowledge_invalid_po_number()`
    Purpose: Test acknowledging a purchase order with an invalid PO number.
- Steps:
    1. Send a PATCH request to the endpoint for acknowledging a purchase order with an invalid PO number.
    2. Assert that the response status code is HTTP 404 NOT FOUND.

### Historical Performance Model API Testing

#### HistoricalPerformanceModelTestCase

#### `setUp()`
    Purpose: Set up necessary objects and data for testing historical performance data.
- Steps:
    1. Create a superuser for testing.
    2. Authenticate the test client with the superuser.
    3. Generate an authentication token for the superuser.
    4. Create a vendor object for testing.
    5. Create a sample historical performance data object for the vendor.

#### `test_get_performance_data()`
    Purpose: Test retrieving historical performance data for a valid vendor.
- Steps:
    1. Send a GET request to the endpoint for retrieving performance data of the vendor.
    2. Assert that the response status code is HTTP 200 OK.
    3. Assert that the response contains data for one historical performance entry.
    4. Assert that the vendor code in the response matches the vendor code used for testing.

#### `test_get_performance_data_invalid_vendor()`
    Purpose: Test retrieving historical performance data for an invalid vendor.
- Steps:
    1. Send a GET request to the endpoint for retrieving performance data of an invalid vendor.
    2. Assert that the response status code is HTTP 404 NOT FOUND.


  ## Authors

- [@ksreyansh](https://www.github.com/ksreyansh/)

  (Thank you for considering my application)
