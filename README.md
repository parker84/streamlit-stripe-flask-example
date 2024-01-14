# Streamlit x Flask x Stripe 🌶️
Monetize your streamlit apps with Stripe and Flask

<img width="1177" alt="image" src="https://github.com/parker84/streamlit-stripe-flask-example/assets/12496987/cd550810-59da-4af3-9ea8-3d676c03181c">

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

See more details here: [Fulfill orders with Stripe Checkout](https://stripe.com/docs/payments/checkout/fulfill-orders)


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

### Now you can visit Your App at `http://localhost:8501`
#### Click `Sign Up`:
<img width="1005" alt="image" src="https://github.com/parker84/streamlit-stripe-flask-example/assets/12496987/00fecb9f-0813-45a4-9516-5dcc6587948c">

#### And this will bring you to the Signup Page
Enter your information and press signup:
<img width="1011" alt="image" src="https://github.com/parker84/streamlit-stripe-flask-example/assets/12496987/5371e09d-39a3-4717-ae27-ac7f010f5daa">

#### Then that will direct you to the Checkout Page
On which you can use a test card (`424242...`) to purchase the product:
<img width="1003" alt="image" src="https://github.com/parker84/streamlit-stripe-flask-example/assets/12496987/9ca1ae93-9843-4642-a826-7e2089ade9ca">
(note it needs to be a test product that you created earlier to use the test card)

#### Which will direct you to the Login Page
Enter your information and click Login
<img width="1007" alt="image" src="https://github.com/parker84/streamlit-stripe-flask-example/assets/12496987/0569361e-e0a0-468d-ba1b-c177f5ed8567">

#### And Voila 🪄
You are logged in and can access Your App:
<img width="1070" alt="image" src="https://github.com/parker84/streamlit-stripe-flask-example/assets/12496987/a64c3f9e-c198-4e01-a7c0-fb608b0a30b7">

And you can also lookup your user in the database and see that they're status is updated to `1` because you successfully completed the stripe checkout process:
<img width="1072" alt="image" src="https://github.com/parker84/streamlit-stripe-flask-example/assets/12496987/a5102742-db35-49b3-affb-2dfdfb98aaae">



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
