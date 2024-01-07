from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import stripe
from decouple import config
from utils.constants import DB_URL
from datetime import datetime
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'), logger=logger)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy()
db.init_app(app)
stripe.api_key = config('STRIPE_API_KEY')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda x: datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=lambda x: datetime.utcnow())
    status = db.Column(db.Integer) # 0 = inactive, 1 = active, 2 = cancelled
    stripe_customer_id = db.Column(db.String, nullable=True, unique=True)
    # data = db.Column(db.JSON, nullable=False, default=lambda: {})

    def __repr__(self):
        return f"<User {self.username}>"


@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    logger.debug('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        logger.error('REQUEST TOO BIG')
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
        logger.error(f'INVALID PAYLOAD, ERROR: {err}')
        return {}, 400
    except stripe.error.SignatureVerificationError as err:
        logger.error(f'INVALID SIGNATURE, ERROR: {err}')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logger.debug(f'session: {session}')
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        logger.debug(f"line_items: {line_items['data'][0]['description']}")
        logger.debug(f"customer: {session['customer']}")
        user = User.query.filter_by(stripe_customer_id=session['customer']).first()
        if user:
            user.status = 1
            db.session.commit()
            logger.info(f"User {user.username} updated to active.")
        else:
            logger.error("User not found.")

    return {}


# TODO: add another webhook for when a user cancels their subscription