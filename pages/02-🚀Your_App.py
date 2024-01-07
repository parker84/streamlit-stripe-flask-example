import streamlit as st
from utils.auth import login_st_form

st.set_page_config(page_title='Streamlit x Flask x Stripe Example', page_icon='🌶️', initial_sidebar_state="auto", menu_items=None)

st.title('🚀 Your Streamlit App')

logged_in = login_st_form()

if logged_in:
    st.success('You are logged in!')
    st.balloons()
    st.markdown('Add Your Streamlit App Here!')
