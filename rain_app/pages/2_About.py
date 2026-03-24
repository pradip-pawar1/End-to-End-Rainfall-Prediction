import streamlit as st

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="Prediction")
st.sidebar.page_link("pages/2_About.py", label="About")
st.sidebar.page_link("pages/3_Model_Insights.py", label="Model Insights")

st.title("About This Project")
st.info(
    "End-to-end machine learning system predicting rainfall using "
    "XGBoost, FastAPI, and Streamlit."
)
st.markdown("---")

# Section 1 - Overview
st.header("Overview")
st.write("""
This application predicts whether it will rain tomorrow based on
daily weather observations. The system uses an XGBoost machine
learning model served through a FastAPI backend and accessed
through a Streamlit web interface.

The goal of the project is to demonstrate a complete end-to-end
machine learning system — from feature engineering and model
training to API deployment and live user interaction.
""")

st.markdown("---")

# Section 2 - Problem Statement
st.header("Problem Statement")
st.write("""
Rainfall prediction is a critical challenge in meteorology and agriculture.
Traditional forecasting methods rely on complex atmospheric models.
This project takes a different approach — using historical weather observations
and machine learning to predict whether it will rain tomorrow.
""")

st.markdown("---")

# Section 3 - Why This Project
st.header("Why This Project")
st.write("""
Most machine learning projects stop at a Jupyter notebook.
This project goes further — the trained model is packaged inside a production
pipeline, served through a REST API, and accessible through a live web interface.
The goal was not just to build a model but to build a system.
""")

st.markdown("---")

# Section 4 - Dataset
st.header("Dataset")
st.write("""
The model was trained on the Australian Weather dataset,
containing daily observations from multiple weather stations.

Each record includes measurements such as temperature,
humidity, pressure, wind speed, cloud cover, and rainfall.
These variables allow the model to learn patterns associated
with rainfall events.
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Features", "21")
with col2:
    st.metric("Feature Type", "Engineered")
with col3:
    st.metric("Algorithm", "XGBoost")

st.markdown("---")

# Section 5 - Feature Engineering
st.header("Feature Engineering")
st.write("""
Raw weather data contains separate readings at 9am and 3pm for most measurements.
Instead of treating these as independent features, meaningful derived features
were engineered to capture more informative patterns for the model.
""")

col1, col2 = st.columns(2)
with col1:
    st.info("""
    **Raw Inputs**

    - Temperature at min and max
    - Humidity at 9am and 3pm
    - Pressure at 9am and 3pm
    - Wind speed at 9am and 3pm
    - Cloud cover at 9am and 3pm
    - Wind directions as angles
    """)

with col2:
    st.success("""
    **Derived Features**

    - Humidity mean and difference
    - Pressure mean and difference
    - Wind speed mean and difference
    - Cloud mean and difference
    - Temperature range and difference
    - Month for seasonal patterns
    """)

st.markdown("---")

# Section 6 - System Architecture
st.header("System Architecture")
st.write("""
The system is built with clear separation of concerns across three layers.
Each layer has a single responsibility and communicates through a defined interface.
""")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.info("**User**\n\nEnters weather data through the Streamlit form interface.")
with col2:
    st.info("**Streamlit UI**\n\nCollects inputs, derives features, sends POST request to API.")
with col3:
    st.warning("**FastAPI Backend**\n\nValidates request schema and routes to the ML pipeline.")
with col4:
    st.warning("**ML Pipeline**\n\nApplies imputation and scaling before passing to model.")
with col5:
    st.success("**XGBoost Model**\n\nReturns probability and final prediction with custom threshold.")

st.markdown("---")

# Section 7 - Why XGBoost
st.header("Why XGBoost")
st.write("""
XGBoost is a gradient boosted decision tree ensemble. It was chosen because
it consistently outperforms other algorithms on structured tabular data,
handles non-linear feature interactions naturally, and is robust to outliers.
It is widely used in both industry and competitive data science for exactly
these reasons.
""")

st.markdown("---")

# Section 8 - Engineering Decisions
st.header("Engineering Decisions")

col1, col2 = st.columns(2)
with col1:
    st.warning("""
    **Custom Probability Threshold**

    Instead of using the default 0.5 threshold, a custom threshold was tuned
    during training to control the precision-recall tradeoff. This is critical
    in forecasting where the cost of missing rain differs from a false alarm.
    """)

with col2:
    st.success("""
    **Pipeline Encapsulation**

    Preprocessing lives inside the Sklearn pipeline alongside the model.
    This ensures identical transformations during training and inference,
    eliminating any risk of data leakage or inconsistency.
    """)

st.markdown("---")

# Section 9 - Author
st.header("Author")
col1, col2 = st.columns(2)
with col1:
    st.info("""
    **Pradip Pawar**

    Machine Learning developer, building production-ready
    data science systems.

    Passionate about transforming data into intelligent applications
    through robust models, scalable APIs, and clean user interfaces.
    """)

with col2:
    st.success("""
    **Links**

    - GitHub: [End-to-End-Rainfall-Prediction](https://github.com/pradip-pawar1/End-to-End-Rainfall-Prediction)
    - API Docs: [rain-prediction-api.onrender.com/docs](https://rain-prediction-api.onrender.com/docs)
    - Live App: [rainfall-prediction-app1.streamlit.app](https://rainfall-prediction-app1.streamlit.app)
    """)

st.caption("Built as part of a self-driven journey into applied machine learning.")