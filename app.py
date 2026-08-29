import streamlit as st
import pandas as pd
import numpy as np
import joblib

import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="💳",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL AND SCALER
# --------------------------------------------------

@st.cache_resource
def load_model():
    model = joblib.load("fraud_detection_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler


model, scaler = load_model()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💳 Credit Card Fraud Detection System")
st.write(
    "Machine Learning based system for detecting fraudulent "
    "credit card transactions."
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Home",
        "🔍 Fraud Detection",
        "📊 Dataset Analysis",
        "📈 Model Performance"
    ]
)

# ==================================================
# HOME PAGE
# ==================================================

if page == "🏠 Home":

    st.header("Welcome to Credit Card Fraud Detection")

    st.write("""
    This application uses a trained Machine Learning model
    to classify credit card transactions as:

    - ✅ Normal Transaction
    - 🚨 Fraudulent Transaction
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Dataset", "Credit Card Transactions")

    with col2:
        st.metric("Features", "30")

    with col3:
        st.metric("Model", "Machine Learning")

    st.info(
        "Use the Fraud Detection page to upload a transaction "
        "CSV file and predict whether transactions are fraudulent."
    )


# ==================================================
# FRAUD DETECTION PAGE
# ==================================================

elif page == "🔍 Fraud Detection":

    st.header("🔍 Fraud Detection")

    st.write(
        "Upload a CSV file containing transaction data. "
        "The file should contain the same transaction features "
        "used during model training."
    )

    uploaded_file = st.file_uploader(
        "Upload Transaction CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        data = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Data")

        st.dataframe(data.head())

        # Remove Class column if user uploaded labelled data
        if "Class" in data.columns:
            X = data.drop("Class", axis=1)
        else:
            X = data.copy()

        # Check required columns
        required_columns = [
            "Time",
            "V1", "V2", "V3", "V4", "V5",
            "V6", "V7", "V8", "V9", "V10",
            "V11", "V12", "V13", "V14", "V15",
            "V16", "V17", "V18", "V19", "V20",
            "V21", "V22", "V23", "V24", "V25",
            "V26", "V27", "V28",
            "Amount"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in X.columns
        ]

        if missing_columns:

            st.error(
                "Missing required columns: "
                + ", ".join(missing_columns)
            )

        else:

            # Arrange columns in correct order
            X = X[required_columns]

            # Scale data
            X_scaled = scaler.transform(X)

            # Make predictions
            predictions = model.predict(X_scaled)

            # Add predictions
            result = data.copy()

            result["Prediction"] = predictions

            result["Result"] = np.where(
                predictions == 1,
                "🚨 FRAUDULENT",
                "✅ NORMAL"
            )

            st.subheader("Prediction Results")

            st.dataframe(result)

            # Statistics
            fraud_count = int(np.sum(predictions == 1))
            normal_count = int(np.sum(predictions == 0))

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Normal Transactions",
                    normal_count
                )

            with col2:
                st.metric(
                    "Fraudulent Transactions",
                    fraud_count
                )

            # Alert
            if fraud_count > 0:

                st.error(
                    f"⚠️ {fraud_count} fraudulent transaction(s) detected!"
                )

            else:

                st.success(
                    "✅ No fraudulent transactions detected."
                )

            # Download results
            csv = result.to_csv(index=False)

            st.download_button(
                label="⬇️ Download Prediction Results",
                data=csv,
                file_name="fraud_detection_results.csv",
                mime="text/csv"
            )


# ==================================================
# DATASET ANALYSIS PAGE
# ==================================================

elif page == "📊 Dataset Analysis":

    st.header("📊 Dataset Analysis")

    try:

        df = pd.read_csv("creditcard.csv")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Transactions",
                f"{len(df):,}"
            )

        with col2:
            st.metric(
                "Total Features",
                len(df.columns) - 1
            )

        with col3:
            fraud_count = int(df["Class"].sum())
            st.metric(
                "Fraud Transactions",
                fraud_count
            )

        st.subheader("Class Distribution")

        class_counts = df["Class"].value_counts()

        st.bar_chart(class_counts)

        st.subheader("Dataset Preview")

        st.dataframe(df.head(10))

        st.subheader("Missing Values")

        missing = df.isnull().sum()

        st.dataframe(
            missing.to_frame("Missing Values")
        )

    except Exception as e:

        st.error(f"Error loading dataset: {e}")


# ==================================================
# MODEL PERFORMANCE PAGE
# ==================================================

elif page == "📈 Model Performance":

    st.header("📈 Model Performance")

    st.write(
        "Performance of the trained fraud detection model."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Accuracy", "99.91%")

    with col2:
        st.metric("Precision", "84.62%")

    with col3:
        st.metric("Recall", "57.89%")

    with col4:
        st.metric("F1 Score", "68.75%")

    st.divider()

    st.subheader("Confusion Matrix")

    # Values obtained from your model evaluation
    cm = np.array([
        [56641, 10],
        [40, 55]
    ])

    fig, ax = plt.subplots()

    ax.imshow(cm)

    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    ax.set_xticklabels(["Normal", "Fraud"])
    ax.set_yticklabels(["Normal", "Fraud"])

    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                cm[i, j],
                ha="center",
                va="center"
            )

    st.pyplot(fig)

    st.info(
        "The model achieved approximately 99.91% accuracy. "
        "Because fraud detection is highly imbalanced, "
        "precision, recall and F1-score are also important."
    )