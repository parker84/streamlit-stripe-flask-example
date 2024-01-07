# Streamlit x Flask x Stripe 🌶️
Monetize your streamlit apps with Stripe and Flask

## Getting Started

### Running the app locally
```sh
# running the streamlit app
streamlit run 🏡Home.py
# running the flask app (for webhooks)
flask --app flask_app run
# Stripe Development Environment:
stripe listen --forward-to 127.0.0.1:5000/stripe_webhook
# Then you can purchase a product from the streamlit app and see the webhook response in the terminal
```

## Understanding the Code

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
