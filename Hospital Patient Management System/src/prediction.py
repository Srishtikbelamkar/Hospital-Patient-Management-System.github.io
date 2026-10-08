import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# PATIENT STATUS PREDICTION
# ============================================================

FEATURES = [
    "Age",
    "Gender",
    "Department",
    "Admission_Type",
    "Insurance_Type",
    "Diagnosis"
]

TARGET = "Patient_Status"


# ============================================================
# PREPARE PATIENT DATA
# ============================================================

def prepare_prediction_data(df):

    data = df.copy()

    required_columns = FEATURES + [TARGET]

    data = data[required_columns].dropna()

    X = data[FEATURES].copy()
    y = data[TARGET].astype(str)

    return X, y


# ============================================================
# TRAIN PATIENT STATUS MODEL
# ============================================================

def train_patient_status_model(df):

    X, y = prepare_prediction_data(df)

    categorical_features = [
        "Gender",
        "Department",
        "Admission_Type",
        "Insurance_Type",
        "Diagnosis"
    ]

    numerical_features = [
        "Age"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            ),
            (
                "numerical",
                "passthrough",
                numerical_features
            )
        ]
    )

    random_forest = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                random_forest
            )
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    pipeline.fit(
        X_train,
        y_train
    )

    predictions = pipeline.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    report = classification_report(
        y_test,
        predictions,
        zero_division=0
    )

    return (
        pipeline,
        accuracy,
        report,
        X_test,
        y_test,
        predictions
    )


# ============================================================
# PREDICT PATIENT STATUS
# ============================================================

def predict_patient_status(
    model,
    patient_data
):

    patient_df = pd.DataFrame(
        [patient_data]
    )

    prediction = model.predict(
        patient_df
    )

    return prediction[0]


# ============================================================
# PREDICTION PROBABILITY
# ============================================================

def predict_patient_status_probability(
    model,
    patient_data
):

    patient_df = pd.DataFrame(
        [patient_data]
    )

    probabilities = model.predict_proba(
        patient_df
    )[0]

    classes = model.classes_

    result = pd.DataFrame(
        {
            "Patient Status": classes,
            "Probability": probabilities * 100
        }
    )

    result["Probability"] = result[
        "Probability"
    ].round(2)

    return result


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

def get_feature_importance(model):

    preprocessor = model.named_steps[
        "preprocessor"
    ]

    random_forest = model.named_steps[
        "model"
    ]

    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    importance = random_forest.feature_importances_

    result = pd.DataFrame(
        {
            "Feature": feature_names,
            "Importance": importance
        }
    )

    result = result.sort_values(
        "Importance",
        ascending=False
    )

    return result


# ============================================================
# PATIENT DEMAND FORECASTING
# ============================================================

def create_demand_forecast(
    df,
    months_to_forecast=6
):

    data = df.copy()

    data["Admission_Date"] = pd.to_datetime(
        data["Admission_Date"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Admission_Date"]
    )

    # --------------------------------------------------------
    # Monthly patient count
    # --------------------------------------------------------

    monthly = (
        data
        .set_index("Admission_Date")
        .resample("MS")
        .size()
        .reset_index(name="Patients")
    )

    if len(monthly) < 6:

        return monthly, pd.DataFrame()

    # --------------------------------------------------------
    # Time features
    # --------------------------------------------------------

    monthly["Year"] = (
        monthly["Admission_Date"]
        .dt.year
    )

    monthly["Month"] = (
        monthly["Admission_Date"]
        .dt.month
    )

    monthly["Time_Index"] = np.arange(
        len(monthly)
    )

    features = [
        "Year",
        "Month",
        "Time_Index"
    ]

    X = monthly[features]

    y = monthly["Patients"]

    # --------------------------------------------------------
    # Forecasting model
    # --------------------------------------------------------

    forecast_model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    forecast_model.fit(
        X,
        y
    )

    # --------------------------------------------------------
    # Future dates
    # --------------------------------------------------------

    last_date = monthly[
        "Admission_Date"
    ].max()

    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=months_to_forecast,
        freq="MS"
    )

    future = pd.DataFrame(
        {
            "Admission_Date": future_dates
        }
    )

    future["Year"] = (
        future["Admission_Date"]
        .dt.year
    )

    future["Month"] = (
        future["Admission_Date"]
        .dt.month
    )

    future["Time_Index"] = np.arange(
        len(monthly),
        len(monthly) + months_to_forecast
    )

    future["Predicted_Patients"] = (
        forecast_model.predict(
            future[features]
        )
    )

    future["Predicted_Patients"] = (
        future["Predicted_Patients"]
        .round()
        .astype(int)
    )

    return monthly, future