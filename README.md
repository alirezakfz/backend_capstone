# Description
This repository contains the capstone project for meta backend development course.
<br> <br>

# Project Structure
The project has two parts. There is `restaurant` app that is frontend part rendering templates. The second app is responsible for endpoint API service with authentication and authorization. There are different hierarchy of user access to the API endpoint that can be defined in the backend for Managers, Customers, Delivery user accounts.

<br> <br>

# Installation

install the dependencies
```jsx
pipenv install
```

Activate the virtual environment

```jsx
pipenv shell
```
<br>

# Setup
The default database settings are

```jsx
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'littlelemon',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'admin',
        'PASSWORD': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}
```
💡 Change those settings according to your local setup.
<br>
<br>

Apply the migrations
```jsx
python manage.py migrate
```
<br>


# API Endpoints
The `api` app has a total of 14 endpoints. Additionally, `Djoser` and `SimpleJWT` endpoints are available.
<br>

Each endpoint requires a SimpleJWT Token for authorization. Pass the token in the header of the request such as
```jsx
{'Authorization': 'JWT <token>'}
```
<br>

In Insomnia, add the token as follows

![Untitled](assets/insomnia.png)
<br>

### Endpoints for `api` app
```jsx
http:<IP-Address>/api/menu-items
http:<IP-Address>/api/menu-items/<int:pk>
http:<IP-Address>/api/bookings
http:<IP-Address>/api/bookings/<int:pk>
http:<IP-Address>/api/categories
http:<IP-Address>/api/groups/manager/users
http:<IP-Address>/api/groups/manager/users/<int:pk>
http:<IP-Address>/api/groups/delivery-crew/users
http:<IP-Address>/api/groups/delivery-crew/users/<int:pk>
http:<IP-Address>/api/cart/menu-items
http:<IP-Address>/api/orders
http:<IP-Address>/api/orders/<int:pk>
http:<IP-Address>/api/cart/orders
http:<IP-Address>/api/cart/orders/<int:pk>
```
<br>

http:<IP-Address>/api/menu-items
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves all menu items | Yes | 200 |
| POST | Creates a menu item | Yes | 201 |
<br>

http:<IP-Address>/api/menu-items/<int:pk>
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves the menu item details | Yes | 200 |
| PUT | Update the menu item | Yes | 200 |
| PATCH | Partially update the menu item | Yes | 200 |
| DELETE | Delete the menu item | Yes | 200 |
<br>

http:<IP-Address>/api/bookings
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves all bookings | Yes | 200 |
| POST | Creates a booking | Yes | 201 |
<br>

http:<IP-Address>/api/bookings/{bookingId}
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves the booking details | Yes | 200 |
| PUT | Update the booking | Yes | 200 |
| PATCH | Partially update the booking | Yes | 200 |
| DELETE | Delete the booking | Yes | 200 |
<br>


http:<IP-Address>/api/categories
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieves all food categories | Yes | 200 |
| POST | Creates new category | Yes | 201 |
<br>

http:<IP-Address>/api/groups/manager/users
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieve all the Manager users| Yes | 200 |
| POST | Add new user to Manager group | Yes | 201 |
<br>

http:<IP-Address>/api/groups/manager/users/<int:pk>
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Get information about single user | Yes | 200 |
| PUT | Add new user as Manager | Yes | 200 |
| PATCH | Update the user profile | Yes | 200 |
| DELETE | Delete the user from Manager group | Yes | 200 |
<br>

http:<IP-Address>/api/groups/delivery-crew/users
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| GET | Retrieve all the Delivery crews| Yes | 200 |
| POST | Add new user to the Delivery-Crew member | Yes | 201 |
<br>

### Endpoints for `djoser` app
```jsx
http:<IP-Address>/auth/users/
http:<IP-Address>/auth/users/me/
http:<IP-Address>/auth/users/confirm/
http:<IP-Address>/auth/users/resend_activation/
http:<IP-Address>/auth/users/set_password/
http:<IP-Address>/auth/users/reset_password/
http:<IP-Address>/auth/users/reset_password_confirm/
http:<IP-Address>/auth/users/set_username/
http:<IP-Address>/auth/users/reset_username/
http:<IP-Address>//auth/users/reset_username_confirm/
```
<br>

http:<IP-Address>/auth/users/
| Method | Action | STATUS CODE | TOKEN AUTH |
| --- | --- | --- | --- |
| GET | Retrieves all users | 200 | No |
| POST | Creates a user | 201 | No |

💡 Please refer to the [Djoser documentation](https://djoser.readthedocs.io/en/latest/getting_started.html#available-endpoints) for further usage on these endpoints.
<br> <br>

### Endpoints for `simplejwt` app
```jsx
http:<IP-Address>/api/token/login/
http:<IP-Address>/api/token/refresh/
```
<br>

http:<IP-Address>/api/token/login/
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| POST | Generates access token and refresh token | Yes | 201 |
<br>

http:<IP-Address>/api/token/refresh/
| Method | Action | TOKEN AUTH | STATUS CODE |
| --- | --- | --- | --- |
| POST | Generates a new access token | Yes | 201 |
<br>

# Testing
There are a total of 12 tests to ensure that each API endpoint and each of its allowed HTTP methods work properly.
<br>

Run the tests
```jsx
python manage.py test restaurant/tests
```
<br>

It should output something similar to this
```jsx
Found 10 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.013s

OK
Destroying test database for alias 'default'...
```
<br>


