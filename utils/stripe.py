from utils.constants import (
    CHECKOUT_SUCCESS_URL, 
    CHECKOUT_CANCEL_URL
)
import stripe
from decouple import config
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'), logger=logger)
stripe.api_key = config('STRIPE_API_KEY')

def get_create_checkout_session_url(customer_email, stripe_customer):
    # read more here: https://stripe.com/docs/checkout/quickstart
    try:
        checkout_session = stripe.checkout.Session.create(
            billing_address_collection='auto',
            customer=stripe_customer.id,
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
        logger.error(f"Error: {e}")
        return str(e)
    return checkout_session.url