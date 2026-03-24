import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# st.set_page_config(page_title="Model Insights - Rainfall Prediction", layout="wide")
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

st.title("Model Insights")
st.markdown("A transparent look at how the model works, what it learned, and how it makes decisions.")
st.markdown("---")

# Section 1 - Model Summary
st.header("Model Summary")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Algorithm", "XGBoost")
with col2:
    st.metric("Decision Threshold", "0.45")
with col3:
    st.metric("Top Feature", "Humidity Mean")
with col4:
    st.metric("Total Features", "21")

st.markdown("---")

# Section 2 - Threshold Explanation
st.header("Why Threshold 0.45?")
st.write("""
By default, most classifiers use a probability threshold of 0.50 to decide between
classes. This project uses a custom threshold of 0.45.

In rainfall prediction, missing a rain event (false negative) is more costly than
a false alarm (false positive). A farmer who is not warned about rain and leaves
crops unprotected suffers real loss. A slightly lower threshold means the model
is more sensitive to rain signals — it will predict rain more readily when conditions
are borderline, which is the safer and more practical decision in a weather system.

This threshold was tuned deliberately during training, not left at default.
""")

st.markdown("---")

# Section 3 - Feature Importance Chart
st.header("Feature Importance")
st.write("""
Feature importance shows how much each input variable contributed to the model's
decisions across all training data. Higher importance means the model relied on
that feature more heavily to split decisions.
""")

features = [
    "Humidity_mean", "Humidity_diff", "Rainfall", "WindGustSpeed", "Sunshine",
    "Pressure_mean", "Cloud_mean", "ClimateZone", "Temp_diff", "Pressure_diff",
    "WindDir3pm_angle", "MaxTemp", "Temp_range", "WindDir9am_angle", "MinTemp",
    "Month", "Cloud_diff", "WindGustDir_angle", "WindSpeed_mean", "WindSpeed_diff",
    "Evaporation"
]

importance_values = [
    0.249553, 0.083422, 0.080634, 0.077276, 0.069857,
    0.055614, 0.044890, 0.042391, 0.034379, 0.030867,
    0.026944, 0.024243, 0.022884, 0.022433, 0.022130,
    0.021435, 0.020310, 0.020124, 0.018830, 0.016130,
    0.015654
]

df = pd.DataFrame({"Feature": features, "Importance": importance_values})
df = df.sort_values("Importance", ascending=True)

colors = ["#1f77b4" if v < 0.05 else "#ff7f0e" if v < 0.10 else "#d62728" for v in df["Importance"]]

fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(df["Feature"], df["Importance"], color=colors)
ax.set_xlabel("Importance Score")
ax.set_title("XGBoost Feature Importance", fontsize=14, fontweight="bold")
ax.axvline(x=0.05, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

low = mpatches.Patch(color="#1f77b4", label="Low (< 0.05)")
mid = mpatches.Patch(color="#ff7f0e", label="Medium (0.05 - 0.10)")
high = mpatches.Patch(color="#d62728", label="High (> 0.10)")
ax.legend(handles=[low, mid, high], loc="lower right")

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# Section 4 - Key Insights from Feature Importance
st.header("What the Model Learned")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Humidity Dominates")
    st.write("""
    Humidity mean alone accounts for nearly 25% of all model decisions.
    Combined with humidity difference, moisture in the air is by far the
    strongest signal for next-day rainfall. This aligns perfectly with
    meteorological understanding — sustained high humidity throughout the
    day is the clearest precursor to rain.
    """)

    st.subheader("Pressure and Wind Matter")
    st.write("""
    Wind gust speed and pressure mean both rank in the top 6 features.
    Dropping pressure combined with strong gusts is a classic storm pattern.
    The model learned this relationship purely from data.
    """)

with col2:
    st.subheader("Today's Rainfall is a Strong Signal")
    st.write("""
    Rainfall today is the third most important feature. If it is already
    raining, conditions that produce rain are clearly present — making
    tomorrow's rain significantly more likely. The model correctly weighted
    this heavily.
    """)

    st.subheader("Sunshine is an Inverse Signal")
    st.write("""
    High sunshine hours today means clear skies, low humidity, and stable
    pressure — conditions that reduce the probability of rain tomorrow.
    The model uses sunshine as a strong negative indicator for rainfall.
    """)

st.markdown("---")

# Section 5 - Pipeline Architecture
st.header("Preprocessing Pipeline")
st.write("""
All preprocessing is encapsulated inside a Sklearn pipeline with three stages.
This ensures that the exact same transformations applied during training are
applied at inference time — no inconsistency, no data leakage.
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Step 1 — Imputer**\n\nMedian imputation fills missing values. Median was chosen over mean because weather data contains outliers that would skew mean-based imputation.")
with col2:
    st.info("**Step 2 — Scaler**\n\nStandardScaler normalizes all features to zero mean and unit variance. This ensures no single feature dominates due to its scale.")
with col3:
    st.info("**Step 3 — XGBoost**\n\nThe gradient boosted classifier makes the final prediction using the cleaned and scaled feature vector.")

st.markdown("---")

# Section 6 - Honest Limitations
st.header("Honest Limitations")
st.write("""
No model is perfect. These are the known limitations of this system:
""")

col1, col2 = st.columns(2)
with col1:
    st.warning("""
    **Geographic Bias**
    The training data is from Australian weather stations.
    Predictions for other geographic regions may be less reliable
    since climate patterns differ significantly.
    """)

with col2:
    st.warning("""
    **No Temporal Context**
    The model treats each day as independent. It does not consider
    sequences of weather days or multi-day trends, which a full
    meteorological model would incorporate.
    """)