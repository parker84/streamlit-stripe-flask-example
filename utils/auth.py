import streamlit as st
from utils.constants import (
    USER_TABLE, 
    LOGIN_URL,
    SIGNUP_URL
)
import jwt
import stripe
from decouple import config
from utils.stripe import get_create_checkout_session_url
import bcrypt
import pandas as pd
import extra_streamlit_components as stx
from utils.validator import Validator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from utils.constants import DB_URL
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL'), logger=logger)
psql_engine = create_engine(DB_URL)
stripe.api_key = config('STRIPE_API_KEY')

@st.cache_resource
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()


# --------------------helpers
# -- encryption
def hash_password(password):
    # Generate a salt and hash the password with the salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(input_password, hashed_password):
    # Check if the input password matches the hashed password
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

# --users
class Authenticator():
    def __init__(self) -> None:
        self.validator = Validator()
        self.cookie_manager = stx.CookieManager()
        self.cookie_name = 'stream_cookie'
        self.key = 'stream_cookie_key'
        self.cookie_expiry_days = 7

        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None
            # TODO: add logout functionality
            # TODO: add reset / forgot password functionality
            # TODO: add google auth functionality
    
    def check_if_user_exists(self, username):
        df = pd.read_sql(f"select * from {USER_TABLE} where username='{username}'", con=psql_engine)
        return df.shape[0] > 0
    
    def register_user(self, username, email, password):
        is_valid_username = self.validator.validate_username(username=username)
        if not is_valid_username:
            raise Exception('Not a valid username')
        is_valid_email = self.validator.validate_email(email=email)
        if not is_valid_email:
            raise Exception('Not a valid email')
        hashed_password = hash_password(password)
        user_exists = self.check_if_user_exists(username=username)
        if user_exists:
            raise Exception('User already exists')
        else:
            stripe_customer = stripe.Customer.create(
                email=email,
            )
            row = {
                'username': username,
                'hashed_password': hashed_password,
                'email': email,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'status': 0, # 0 = inactive, 1 = active, 2 = cancelled
                'stripe_customer_id': stripe_customer.id,
                # 'data': {}
            }
            # TODO: migrate this to using models / sqlalchemy
            row_df = pd.DataFrame([row])
            logger.info(f"Row being added to {USER_TABLE}: \n{row_df}")
            row_df.to_sql(USER_TABLE, if_exists='append', con=psql_engine, index=False)
            return stripe_customer
    
    def check_if_authenticated(self):
        if st.session_state['authentication_status']:
            return True
        else:
            self._check_cookie()
            if st.session_state['authentication_status']:
                return True
            else:
                return False

    def check_user_login(self, username, password):
        df = pd.read_sql(f"select * from {USER_TABLE} where username='{username}'", con=psql_engine)
        if df.shape[0] > 0:
            hashed_pwd = df['hashed_password'].iloc[0]
            correct_password = verify_password(input_password=password, hashed_password=hashed_pwd.tobytes())
            if correct_password and df['status'].iloc[0] == 1:
                st.session_state['username'] = username
                st.session_state['authentication_status'] = True
                self.exp_date = self._set_exp_date()
                self.token = self._token_encode()
                self.cookie_manager.set(self.cookie_name, self.token,
                    expires_at=datetime.utcnow() + timedelta(days=self.cookie_expiry_days))
                return True
            else:
                return False
        else:
            return False
    
    def _token_encode(self) -> str:
        """
        Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        # grabbed from here: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/streamlit_authenticator/authenticate.py
        return jwt.encode({
            # 'name':st.session_state['name'],
            'username':st.session_state['username'],
            'exp_date':self.exp_date}, self.key, algorithm='HS256')

    def _token_decode(self) -> str:
        """
        Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        # grabbed from here: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/streamlit_authenticator/authenticate.py
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> str:
        """
        Creates the reauthentication cookie's expiry date.

        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        # grabbed from here: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/streamlit_authenticator/authenticate.py
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        # grabbed from here: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/streamlit_authenticator/authenticate.py
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = self._token_decode()
            if self.token is not False:
                if not st.session_state['logout']:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'name' and 'username' in self.token:
                            # st.session_state['name'] = self.token['name']
                            st.session_state['username'] = self.token['username']
                            st.session_state['authentication_status'] = True


# ------------streamlit forms

def create_account_st_form():
    st.subheader('Create Account')
    st.caption(f"Already have an account? [Log in here]({LOGIN_URL})")
    authenticator = Authenticator()
    email = st.text_input('Email')
    username = st.text_input('Username').lower()
    password = st.text_input('Password', type='password')
    if email != '' and username != '' and password != '':
        # TODO: we need better logic here to ensure the account isn't being created before the
        # user is actually ready (otherwise we're getting "that account already exists" issues)
        stripe_customer = authenticator.register_user(username=username, email=email, password=password)
        checkout_session_url = get_create_checkout_session_url(email, stripe_customer)
        st.link_button('Sign Up', url=checkout_session_url, type='primary')
    else:
        try_to_sign_up = st.button('Sign Up')
        if try_to_sign_up:
            st.warning('Please enter your information above 👆🏻')

def login_st_form() -> bool:
    authentication_status = None
    authenticator = Authenticator()
    authenticated = authenticator.check_if_authenticated()
    logger.debug(f'st.session_state: {st.session_state}') 
    if authenticated:
        return True
    else:  
        placeholder = st.empty()
        with placeholder.form('Login', clear_on_submit=True):
            st.subheader('Login')
            username = st.text_input('Username').lower()
            password = st.text_input('Password', type='password')
            submit = st.form_submit_button('Submit')
            if submit:
                authentication_status = authenticator.check_user_login(username=username, password=password)
                st.session_state['authentication_status'] = authentication_status
                logger.debug(f'st.session_state: {st.session_state}')
        if authentication_status:
            placeholder.empty()
            return True
        elif authentication_status == False:
            st.error(f"Username/password is incorrect. Don't have an account yet? Create one here: [Sign Up](http://localhost:8501/Sign_Up)")
            return False
        elif authentication_status is None:
            st.warning(f"Don't have an account yet? Create one here: [Sign Up]({SIGNUP_URL})")
            return False