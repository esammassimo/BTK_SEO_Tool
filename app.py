import os
from apikey import apikey

import streamlit as st
if "shared" not in st.session_state:
    st.session_state["shared"] = True
    
st.title("🔗SEO Tools")
