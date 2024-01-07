from utils.constants import (
    CHECKOUT_SUCCESS_URL, 
    CHECKOUT_CANCEL_URL
)
import stripe
from decouple import config
stripe.api_key = config('STRIPE_API_KEY')

def get_create_checkout_session_url(customer_email):
    # read more here: https://stripe.com/docs/checkout/quickstart
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=customer_email,
            billing_address_collection='auto',
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # 'price': 'price_1OPSCoEwJbHfXXR0n1rk3bXL', # live product (use with live api key)
                    'price': 'price_1OUU3tEwJbHfXXR0LqUx1ePh', # test product (use with test api key)
                    'quantity': 1,
                },
            ],
            # mode='subscription',
            mode='payment',
            success_url=CHECKOUT_SUCCESS_URL,
            cancel_url=CHECKOUT_CANCEL_URL,
        )
    except Exception as e:
        return str(e)
    return checkout_session.url