import streamlit as st

st.set_page_config(page_title="Rainfall Prediction", page_icon="🌧️", layout="wide")

# Hide default nav
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Custom navigation
st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="Prediction")
st.sidebar.page_link("pages/2_About.py", label="About")
st.sidebar.page_link("pages/3_Model_Insights.py", label="Model Insights")

st.switch_page("pages/1_Prediction.py")