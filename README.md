# Django E-commerce Store

This is an E-commerce web application built completely with Django for the backend and templates from bootstrap for the frontend.
The application enables merchants to sell their products, manage the store, receive payments using Paypal and card payments handled by Flutterwave's Rave V2 API and also manage the orders received from customers.
- - - -

## Features of the application

* A store for buying and selling products.
* An admin area for managing and updating the store and orders received from customers.
  * Add new products too the store.
  * Delete products from the store
  * Update product information.
  * Create different categories for products on the store.
  * Enable and disable user accounts.
  * View orders created by customers
* A CRUD app for customer addresses available to customers.
* Customer's wishlist section available to customers.
* Paypal integration for payments through paypal.
* Flutterwave integration for card payments.
* Can be used without need for extra code.

## Installation

* Clone this repository: `git clone "https://github.com/victornnamdii/django-ecommerce-app.git"`
* Access the directory: `cd django-ecommerce-app`
* Create virtual environment (optional):

```bash
python3 -m venv venv
source venv/bin/activate
```

* Install application requirements: `pip install -r requirements.txt`

## Starting the Application

**With both Paypal and Flutterwave keys available:**
Open the file `runstore` and insert your keys in the appropriate places and run the command:
```./runstore``` and open `127.0.0.1:8000` in your browser.

**Without Paypal or Flutterwave keys available (payments would not work):**
Run the command: ```./runstore```
and open `127.0.0.1:8000` in your browser.
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image3.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image18.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image19.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image20.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image21.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image17.png?raw=true)
> Screenshots taken on Google Chrome.

If running in production, please open `core/settings/base.py` and change DEBUG to False

## Create Admin User

To create an admin user with permissions to manage the store, run the command:
```python manage.py createsuperuser```
and follow the instructions.

## Using the Admin area

Open `127.0.0.1:8000/admin` in your browser and log in with your details to enter the admin area.
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image.png?raw=true)
> Screenshots taken on Google Chrome

### Accounts

Here, you can create, read, update and delete user accounts.

![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image8.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image9.png?raw=true)
> Screenshots taken on Google Chrome

### Delivery Options

Here, you can add new delivery methods to the store with their prices and delivery times.

![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image6.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image7.png?raw=true)
> Admin Side (screenshots taken on Google Chrome)

![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image15.png?raw=true)
> Customer side (screenshots taken on Google Chrome)

### Orders

![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image2.png?raw=true)
> Admin side

![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image16.png?raw=true)
> Customer side (screenshots taken on Google Chrome)

Here, the admin user can see orders that have been made by customers and can also filter the results depending on the date created, if it has been shipped and also their billing status.
Clicking on any of the orders give you full information about them.

![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image4.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image5.png?raw=true)
> Screenshots taken on Google Chrome

You can also update the orders to show that they've been shipped/processed.

### Categories, Product Types, Products

Here, you can create, read, update and delete new products, the categories they belong to and their product types.
> Product Types are a sub-section of Categories. E.g a Music Tape is a product type, Tape is the Categoory.

![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image10.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image11.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image12.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image13.png?raw=true)
![alt text](https://github.com/victornnamdii/django-ecommerce-app/blob/main/_images/image14.png?raw=true)
> Screenshots taken on Google Chrome
