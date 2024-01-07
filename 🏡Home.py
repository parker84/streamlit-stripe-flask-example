import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='Streamlit x Flask x Stripe Example', page_icon='🌶️', initial_sidebar_state="auto", menu_items=None)

st.title('Streamlit x Flask x Stripe 🌶️')


st.markdown(    
    """
### Monetize Your Streamlit App
Simple example on how to create a streamlit app with gated user access to paying subscribers using stripe and flask.
    """)


sign_up = st.button('Sign Up', type='primary')
if sign_up:
    switch_page('sign up')