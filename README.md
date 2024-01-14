# Streamlit x Flask x Stripe 🌶️
Monetize your streamlit apps with Stripe and Flask

## Purpose
The purpose of this repo is to show you how you can create streamlit app that requires authenticated users to pay for access to it, using Stripe and Flask.

## Getting Started

### Setting up the Db
This is where your users will be stored:
1. Create a postgres database
2. Run the `utils/db_setup.sql` script to create the `users` table

### Setting up Stripe:
1. Create a Stripe account
2. Create a test product
3. Grab the `price_id` from the product

See more details here: [Accept Payments with Stripe Checkout](https://stripe.com/docs/checkout/quickstart)

### Setting up the Environment
Create a virtual environment and install the requirements:
```sh
virtualenv venv -p python3.10
source venv/bin/activate
pip install -r requirements.txt
```

### Setup Stripe Port Forwarding
We need to setup port forwarding so that Stripe can send webhooks to our local machine.
```sh
# install stripe cli
brew install stripe/stripe-cli/stripe

# forward stripe webhooks to our local machine
stripe listen --forward-to 127.0.0.1:5000/stripe_webhook
```
In the output from this grab the `endpoint_secret` and add it to your .env file.


### Set Environmental Variables

Create a .env file in the root of the project and add the following variables:
```sh
# stripe variables
STRIPE_API_KEY = sk_test_...
STRIPE_ENDPOINT_SECRET = whsec_...

# database variable
DB_USER = ...
DB_PWD = ...
DB_HOST = ...
DB_PORT = ...
DB_NAME = ...

# logging
LOG_LEVEL=INFO
```

### Launch the App Locally
```sh
source ./venv/bin/activate
# running the streamlit app
streamlit run 🏡Home.py
# in a seperate terminal run the flask app (for webhooks)
flask --app flask_app run
```

## Understanding the Code

### Authentication
Our user authentication is loosely based on [streamlit-authenticator](https://github.com/mkhorasani/Streamlit-Authenticator) but we're writing users to a database instead of storing in a file. 

See `utils/auth.py` for the authentication code.

### Accepting Payments
We will be using Stripe to accept payments. Stripe is a payment processing platform that allows you to accept payments and manage your business.

Look at `get_create_checkout_session_url` in `utils/stripe.py` to see how we create a checkout session. 


### Webhooks
We need a way of verifying that the payment was successful. We can do this by using webhooks. 

Webhooks are a way of sending a message from one application to another when something happens. In this case, we want stripe to send a message to our streamlit app when a payment is successful.

See the `stripe_webhook` function in `flask_app.py` to see how we handle the webhook.

## Helpful Resources
- [Accepting Payments in Flask Using Stripe Checkout](https://www.youtube.com/watch?v=cC9jK3WntR8) (stripe webhooks at 22 minutes)
  - [See Full Code Here](https://prettyprinted.com/l/ccJ)
- [Accept Payments with Stripe Checkout](https://stripe.com/docs/checkout/quickstart)
- [Fulfill orders with Stripe Checkout](https://stripe.com/docs/payments/checkout/fulfill-orders)
