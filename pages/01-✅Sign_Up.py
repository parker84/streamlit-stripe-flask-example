import streamlit as st
from utils.auth import create_account_st_form
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='Streamlit x Flask x Stripe Example', page_icon='🌶️', initial_sidebar_state="auto", menu_items=None)

if create_account_st_form():
    switch_page('your app')