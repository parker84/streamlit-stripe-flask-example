from flask import Flask, request, abort
import stripe
from decouple import config

app = Flask(__name__)
stripe.api_key = config('STRIPE_API_KEY')

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = config('STRIPE_ENDPOINT_SECRET')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as err:
        print(f'INVALID PAYLOAD, ERROR: {err}')
        return {}, 400
    except stripe.error.SignatureVerificationError as err:
        print(f'INVALID SIGNATURE, ERROR: {err}')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f'session: {session}')
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(f"line_items: {line_items['data'][0]['description']}")
        # here is where we can fulfill the order, send a confirmation email, etc

    return {}