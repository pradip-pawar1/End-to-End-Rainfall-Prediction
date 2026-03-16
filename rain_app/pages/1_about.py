import streamlit as st

st.set_page_config(page_title="About - Rainfall Prediction", layout="wide")

st.title("About This Project")
st.markdown("---")


# Section 1 - Problem Statement
st.header("Overview")

st.write("""
This application predicts whether it will rain tomorrow based on
daily weather observations. The system uses an XGBoost machine
learning model served through a FastAPI backend and accessed
through a Streamlit web interface.

The goal of the project is to demonstrate a complete end-to-end
machine learning system — from feature engineering and model
training to API deployment and lvjive user interaction.
""")

st.header("Problem Statement")
st.write("""
Rainfall prediction is a critical challenge in meteorology and agriculture.
Traditional forecasting methods rely on complex atmospheric models.
This project takes a different approach — using historical weather observations
and machine learning to predict whether it will rain tomorrow.
""")

st.markdown("---")

# Section 2 - Why This Project
st.header("Why This Project")
st.write("""
Most machine learning projects stop at a Jupyter notebook.
This project goes further — the trained model is packaged inside a production
pipeline, served through a REST API, and accessible through a live web interface.
The goal was not just to build a model but to build a system.
""")

st.markdown("---")

# Section 3 - Dataset
st.header("Dataset")
st.write("""
The model was trained on Australian weather data containing daily observations
from multiple weather stations. The dataset includes temperature, humidity,
wind speed, pressure, cloud cover, and rainfall measurements.
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Features", "21")
with col2:
    st.metric("Feature Type", "Engineered")
with col3:
    st.metric("Algorithm", "XGBoost")

st.markdown("---")

# Section 4 - Feature Engineering
st.header("Feature Engineering")
st.write("""
Raw weather data contains separate readings at 9am and 3pm for most measurements.
Instead of treating these as independent features, meaningful derived features
were engineered to expose stronger signal to the model.
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Raw Inputs")
    st.write("""
    - Temperature at min and max
    - Humidity at 9am and 3pm
    - Pressure at 9am and 3pm
    - Wind speed at 9am and 3pm
    - Cloud cover at 9am and 3pm
    - Wind directions as angles
    """)

with col2:
    st.subheader("Derived Features")
    st.write("""
    - Humidity mean and difference
    - Pressure mean and difference
    - Wind speed mean and difference
    - Cloud mean and difference
    - Temperature range and difference
    - Month for seasonal patterns
    """)

st.markdown("---")

# Section 5 - System Architecture
st.header("System Architecture")
st.write("""
The system is built with clear separation of concerns across three layers.
Each layer has a single responsibility and communicates through a defined interface.
""")

st.code("""
User Input (Streamlit UI)
        |
        v
  HTTP POST Request
        |
        v
FastAPI Backend (/predict)
        |
        ├── Pydantic Input Validation
        ├── Feature Order Control
        ├── Sklearn Pipeline (Imputation + Scaling)
        |
        v
XGBoost Classifier
        |
        v
Probability Score → Custom Threshold → Final Prediction
        |
        v
Structured JSON Response → UI Display
""", language="text")

st.markdown("---")

# Section 6 - Why XGBoost
st.header("Why XGBoost")
st.write("""
XGBoost is a gradient boosted decision tree ensemble. It was chosen because
it consistently outperforms other algorithms on structured tabular data,
handles non-linear feature interactions naturally, and is robust to outliers.
It is widely used in both industry and competitive data science for exactly
these reasons.
""")

st.markdown("---")

# Section 7 - Production Decisions
st.header("Engineering Decisions")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Custom Probability Threshold")
    st.write("""
    Instead of using the default 0.5 threshold, a custom threshold was tuned
    during training to control the precision-recall tradeoff. This is critical
    in forecasting where the cost of missing rain differs from a false alarm.
    """)

with col2:
    st.subheader("Pipeline Encapsulation")
    st.write("""
    Preprocessing lives inside the Sklearn pipeline alongside the model.
    This ensures identical transformations during training and inference,
    eliminating any risk of data leakage or inconsistency.
    """)

st.markdown("---")

# Section 8 - Author
st.header("Author")
col1, col2 = st.columns(2)
with col1:
    st.write("""
    **Pradip**
    Civil Engineering Student | Self-taught ML and Data Science Engineer

    Building toward a future in AI/ML and Data Science through disciplined,
    sequential learning and real-world end-to-end projects.
    """)
with col2:
    st.write("""
    **Links**
    - GitHub: [End-to-End-Rainfall-Prediction](https://github.com/pradip-pawar1/End-to-End-Rainfall-Prediction)
    - API Docs: [rain-prediction-api.onrender.com/docs](https://rain-prediction-api.onrender.com/docs)
    - Live App: [rainfall-prediction-app1.streamlit.app](https://rainfall-prediction-app1.streamlit.app)
    """)