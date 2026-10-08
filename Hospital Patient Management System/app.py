import streamlit as st
import pandas as pd
import os
import sys
import requests
import folium
from streamlit_folium import st_folium

from Hospital_database import (
    create_database,
    save_incident,
    get_incidents
)

# Create SQLite database
create_database()

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hospital Patient Management System",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    PROJECT_DIR,
    "data",
    "hospital_patient.csv"
)

SRC_DIR = os.path.join(
    PROJECT_DIR,
    "src"
)

sys.path.insert(0, SRC_DIR)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    df["Admission_Date"] = pd.to_datetime(
        df["Admission_Date"],
        errors="coerce"
    )

    df["Discharge_Date"] = pd.to_datetime(
        df["Discharge_Date"],
        errors="coerce"
    )

    df["Admission_Year"] = df["Admission_Date"].dt.year

    df["Month_Year"] = (
        df["Admission_Date"]
        .dt.to_period("M")
        .astype(str)
    )

    return df


df = load_data()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "admin123"
    }


# ============================================================
# HOSPITAL BACKGROUND
# ============================================================
import base64

def set_background(image_path):

    with open(image_path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        /* Full background image */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Remove white main content background */
        .main {{
            background: transparent !important;
        }}

        /* Make the main Streamlit container transparent */
        .block-container {{
            background: transparent !important;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        /* Remove white background from forms */
        div[data-testid="stForm"] {{
            background: rgba(255, 255, 255, 0.12) !important;
            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 18px;
            padding: 25px;
            backdrop-filter: blur(4px);
        }}

        /* Transparent tabs area */
        div[data-testid="stTabs"] {{
            background: transparent !important;
        }}

        /* Input boxes */
        div[data-baseweb="input"] {{
            background: rgba(255, 255, 255, 0.70) !important;
            border-radius: 8px;
        }}

        /* Buttons */
        .stButton > button {{
            width: 100%;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid rgba(50, 80, 100, 0.3);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# Apply background
set_background("images/hospital_background.png")

# ============================================================
# LOGIN PAGE CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .login-box {{
        max-width: 430px;
        margin: 60px auto 0 auto;
        padding: 30px;
        background: rgba(255, 255, 255, 0.96);
        border-radius: 18px;
        box-shadow: 0px 5px 25px rgba(0, 0, 0, 0.18);
    }}

    .login-title {{
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #0B4F6C;
        margin-bottom: 5px;
    }}

    .login-subtitle {{
        text-align: center;
        color: #666;
        font-size: 15px;
        margin-bottom: 20px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOGIN / SIGN UP / FORGOT PASSWORD
# ============================================================

if not st.session_state.logged_in:

    # Center the login area
    left_space, center_space, right_space = st.columns(
        [1, 2, 1]
    )

    with center_space:

        st.markdown(
            '<div class="login-container">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-title">'
            '🏥 Hospital Patient Management'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-subtitle">'
            'Secure Hospital Management Portal'
            '</div>',
            unsafe_allow_html=True
        )

        login_tab, signup_tab, forgot_tab = st.tabs(
            [
                "🔐 Login",
                "📝 Sign Up",
                "🔑 Forgot Password"
            ]
        )

        # ====================================================
        # LOGIN
        # ====================================================

        with login_tab:

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            st.checkbox(
                "Remember me",
                key="remember_me"
            )

            if st.button(
                "Login",
                type="primary",
                use_container_width=True
            ):

                if username in st.session_state.users:

                    if (
                        st.session_state.users[username]
                        == password
                    ):

                        st.session_state.logged_in = True
                        st.session_state.username = username

                        st.rerun()

                    else:

                        st.error(
                            "Incorrect password."
                        )

                else:

                    st.error(
                        "Username not found."
                    )

        # ====================================================
        # SIGN UP
        # ====================================================

        with signup_tab:

            new_username = st.text_input(
                "Username",
                key="new_username"
            )

            new_password = st.text_input(
                "Password",
                type="password",
                key="new_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="confirm_password"
            )

            if st.button(
                "Create Account",
                type="primary",
                use_container_width=True
            ):

                if new_username == "":

                    st.warning(
                        "Enter username."
                    )

                elif new_password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                elif new_username in st.session_state.users:

                    st.error(
                        "Username already exists."
                    )

                else:

                    st.session_state.users[
                        new_username
                    ] = new_password

                    st.success(
                        "Account created successfully."
                    )

        # ====================================================
        # FORGOT PASSWORD
        # ====================================================

        with forgot_tab:

            forgot_username = st.text_input(
                "Username",
                key="forgot_username"
            )

            reset_password = st.text_input(
                "New Password",
                type="password",
                key="reset_password"
            )

            confirm_reset = st.text_input(
                "Confirm Password",
                type="password",
                key="reset_confirm"
            )

            if st.button(
                "Reset Password",
                type="primary",
                use_container_width=True
            ):

                if forgot_username not in st.session_state.users:

                    st.error(
                        "Username not found."
                    )

                elif reset_password != confirm_reset:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    st.session_state.users[
                        forgot_username
                    ] = reset_password

                    st.success(
                        "Password reset successfully."
                    )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    st.stop()
def geocode_address(address):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "HospitalPatientManagementSystem/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return None

    return (
        float(data[0]["lat"]),
        float(data[0]["lon"]),
        data[0]["display_name"]
    )


def get_route(
    start_lat,
    start_lon,
    end_lat,
    end_lon
):

    url = (
        "https://router.project-osrm.org/"
        f"route/v1/driving/"
        f"{start_lon},{start_lat};"
        f"{end_lon},{end_lat}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if (
        data.get("code") != "Ok"
        or not data.get("routes")
    ):
        return None

    route = data["routes"][0]

    return {
        "distance_km": route["distance"] / 1000,
        "duration_min": route["duration"] / 60,
        "geometry": route["geometry"]
    }
# ============================================================
# SIDEBAR AFTER LOGIN
# ============================================================

st.sidebar.title("🏥 Hospital Management")

st.sidebar.success(
    f"Welcome, {st.session_state.username}"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Patient Records",
        "📊 Patient Analytics",
        "🔮 Prediction & Forecasting",
        "🛏️ Resource Optimization",
        "⚠️ Incident Reporting",
        "🚑 Ambulance Dispatch",
        "🔔 Alerts & Notifications",
        "📄 History & Reports",
        "⚙️ Profile & Settings"
    ]
)

st.sidebar.markdown("---")


# ============================================================
# LOGOUT
# ============================================================

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">'
        'Hospital Patient Management System'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Patient Management, Analytics and Hospital Operations'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    total_patients = len(df)

    total_revenue = df["Total_Bill"].sum()

    average_bill = df["Total_Bill"].mean()

    departments = df["Department"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👥 Total Patients",
            f"{total_patients:,}"
        )

    with col2:
        st.metric(
            "💰 Total Revenue",
            f"₹{total_revenue:,.0f}"
        )

    with col3:
        st.metric(
            "🧾 Average Bill",
            f"₹{average_bill:,.0f}"
        )

    with col4:
        st.metric(
            "🏥 Departments",
            departments
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏥 Department Overview")

        department_data = (
            df["Department"]
            .value_counts()
            .reset_index()
        )

        department_data.columns = [
            "Department",
            "Patients"
        ]

        st.dataframe(
            department_data,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        st.subheader("🚑 Admission Overview")

        admission_data = (
            df["Admission_Type"]
            .value_counts()
            .reset_index()
        )

        admission_data.columns = [
            "Admission Type",
            "Patients"
        ]

        st.dataframe(
            admission_data,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PATIENT RECORDS
# ============================================================

elif page == "👤 Patient Records":

    st.title("👤 Patient Records")

    search = st.text_input(
        "🔍 Search Patient",
        placeholder="Enter patient name or Patient ID"
    )

    filtered_df = df.copy()

    if search:

        search_text = search.lower()

        filtered_df = filtered_df[
            filtered_df["Patient_Name"]
            .astype(str)
            .str.lower()
            .str.contains(search_text)
            |
            filtered_df["Patient_ID"]
            .astype(str)
            .str.lower()
            .str.contains(search_text)
        ]

    st.write(
        f"Showing {len(filtered_df)} patient records"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PATIENT ANALYTICS
# ============================================================

elif page == "📊 Patient Analytics":

    st.title("📊 Patient Analytics")

    from Graphs import (
        yearly_patient_trend,
        monthly_patient_trend,
        department_graph,
        admission_type_graph,
        payment_status_graph,
        patient_status_graph,
        yearly_revenue_graph
    )

    years = sorted(
        df["Admission_Year"]
        .dropna()
        .unique()
    )

    selected_years = st.multiselect(
        "Select Year",
        years,
        default=years
    )

    analytics_df = df[
        df["Admission_Year"].isin(selected_years)
    ]

    st.subheader("1. Yearly Patient Trend")

    st.plotly_chart(
        yearly_patient_trend(analytics_df),
        use_container_width=True
    )

    st.subheader("2. Monthly Patient Trend")

    st.plotly_chart(
        monthly_patient_trend(analytics_df),
        use_container_width=True
    )

    st.subheader("3. Department Graph")

    st.plotly_chart(
        department_graph(analytics_df),
        use_container_width=True
    )

    st.subheader("4. Admission Type")

    st.plotly_chart(
        admission_type_graph(analytics_df),
        use_container_width=True
    )

    st.subheader("5. Payment Status")

    st.plotly_chart(
        payment_status_graph(analytics_df),
        use_container_width=True
    )

    st.subheader("6. Patient Status")

    st.plotly_chart(
        patient_status_graph(analytics_df),
        use_container_width=True
    )

    st.subheader("7. Yearly Revenue")

    st.plotly_chart(
        yearly_revenue_graph(analytics_df),
        use_container_width=True
    )

# ============================================================
# PREDICTION & FORECASTING
# ============================================================

elif page == "🔮 Prediction & Forecasting":

    st.title("🔮 Prediction & Forecasting")

    st.write(
        "Machine learning based patient status prediction "
        "and patient demand forecasting."
    )

    # --------------------------------------------------------
    # IMPORT ML FUNCTIONS
    # --------------------------------------------------------

    from src.prediction import (
        train_patient_status_model,
        predict_patient_status,
        predict_patient_status_probability,
        get_feature_importance,
        create_demand_forecast
    )

    try:

        # ====================================================
        # TRAIN PATIENT STATUS MODEL
        # ====================================================

        (
            model,
            accuracy,
            report,
            X_test,
            y_test,
            predictions
        ) = train_patient_status_model(df)

        # ====================================================
        # MODEL INFORMATION
        # ====================================================

        st.subheader("🤖 Machine Learning Model")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Model",
                "Random Forest"
            )

        with col2:

            st.metric(
                "Testing Records",
                len(y_test)
            )

        with col3:

            st.metric(
                "Model Accuracy",
                f"{accuracy * 100:.2f}%"
            )

        st.success(
            "Machine learning model trained successfully."
        )

        # ====================================================
        # PATIENT STATUS PREDICTION
        # ====================================================

        st.markdown("---")

        st.subheader(
            "👤 Patient Status Prediction"
        )

        patient_index = st.selectbox(
            "Select Patient",
            range(len(df)),
            format_func=lambda x:
                f"{df.iloc[x]['Patient_ID']} - "
                f"{df.iloc[x]['Patient_Name']}"
        )

        selected_patient = df.iloc[
            patient_index
        ]

        patient_data = {

            "Age":
                selected_patient["Age"],

            "Gender":
                selected_patient["Gender"],

            "Department":
                selected_patient["Department"],

            "Admission_Type":
                selected_patient["Admission_Type"],

            "Insurance_Type":
                selected_patient["Insurance_Type"],

            "Diagnosis":
                selected_patient["Diagnosis"]
        }

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        predicted_status = predict_patient_status(
            model,
            patient_data
        )

        st.success(
            f"Predicted Patient Status: "
            f"{predicted_status}"
        )

        # ====================================================
        # PATIENT DETAILS
        # ====================================================

        st.subheader(
            "📋 Selected Patient Details"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                f"**Patient ID:** "
                f"{selected_patient['Patient_ID']}"
            )

            st.write(
                f"**Patient Name:** "
                f"{selected_patient['Patient_Name']}"
            )

            st.write(
                f"**Age:** "
                f"{selected_patient['Age']}"
            )

        with col2:

            st.write(
                f"**Gender:** "
                f"{selected_patient['Gender']}"
            )

            st.write(
                f"**Department:** "
                f"{selected_patient['Department']}"
            )

            st.write(
                f"**Admission Type:** "
                f"{selected_patient['Admission_Type']}"
            )

        with col3:

            st.write(
                f"**Insurance:** "
                f"{selected_patient['Insurance_Type']}"
            )

            st.write(
                f"**Diagnosis:** "
                f"{selected_patient['Diagnosis']}"
            )

            st.write(
                f"**Actual Status:** "
                f"{selected_patient['Patient_Status']}"
            )

        # ====================================================
        # PREDICTION PROBABILITY
        # ====================================================

        st.markdown("---")

        st.subheader(
            "📊 Prediction Probability"
        )

        probability_df = (
            predict_patient_status_probability(
                model,
                patient_data
            )
        )

        import plotly.express as px

        probability_fig = px.bar(
            probability_df,
            x="Patient Status",
            y="Probability",
            text="Probability",
            title="Patient Status Prediction Probability"
        )

        probability_fig.update_layout(
            xaxis_title="Patient Status",
            yaxis_title="Probability (%)"
        )

        probability_fig.update_traces(
            texttemplate="%{text}%",
            textposition="outside"
        )

        st.plotly_chart(
            probability_fig,
            use_container_width=True
        )

        # ====================================================
        # FEATURE IMPORTANCE
        # ====================================================

        st.subheader(
            "📈 Feature Importance"
        )

        importance_df = (
            get_feature_importance(model)
            .head(10)
            .copy()
        )

        importance_fig = px.bar(
            importance_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Important Factors Used by the Model"
        )

        importance_fig.update_layout(
            xaxis_title="Importance",
            yaxis_title="Feature"
        )

        st.plotly_chart(
            importance_fig,
            use_container_width=True
        )

        # ====================================================
        # PATIENT DEMAND FORECASTING
        # ====================================================

        st.markdown("---")

        st.subheader(
            "🔮 Patient Demand Forecasting"
        )

        st.write(
            "The model estimates future monthly patient demand "
            "using historical admission data."
        )

        monthly_data, forecast_data = (
            create_demand_forecast(
                df,
                months_to_forecast=6
            )
        )

        if not forecast_data.empty:

            # ------------------------------------------------
            # Historical data
            # ------------------------------------------------

            historical_plot = monthly_data[
                [
                    "Admission_Date",
                    "Patients"
                ]
            ].copy()

            historical_plot[
                "Type"
            ] = "Actual"

            historical_plot = historical_plot.rename(
                columns={
                    "Patients":
                    "Patient_Count"
                }
            )

            # ------------------------------------------------
            # Forecast data
            # ------------------------------------------------

            forecast_plot = forecast_data[
                [
                    "Admission_Date",
                    "Predicted_Patients"
                ]
            ].copy()

            forecast_plot[
                "Type"
            ] = "Forecast"

            forecast_plot = forecast_plot.rename(
                columns={
                    "Predicted_Patients":
                    "Patient_Count"
                }
            )

            # ------------------------------------------------
            # Combine
            # ------------------------------------------------

            forecast_chart_data = pd.concat(
                [
                    historical_plot,
                    forecast_plot
                ],
                ignore_index=True
            )

            # ------------------------------------------------
            # Forecast chart
            # ------------------------------------------------

            forecast_fig = px.line(
                forecast_chart_data,
                x="Admission_Date",
                y="Patient_Count",
                color="Type",
                markers=True,
                title="Monthly Patient Demand Forecast"
            )

            forecast_fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Number of Patients"
            )

            st.plotly_chart(
                forecast_fig,
                use_container_width=True
            )

            # ------------------------------------------------
            # Forecast table
            # ------------------------------------------------

            st.subheader(
                "📅 Next 6 Months Forecast"
            )

            display_forecast = forecast_data[
                [
                    "Admission_Date",
                    "Predicted_Patients"
                ]
            ].copy()

            display_forecast[
                "Admission_Date"
            ] = display_forecast[
                "Admission_Date"
            ].dt.strftime(
                "%B %Y"
            )

            display_forecast.columns = [
                "Month",
                "Predicted Patients"
            ]

            st.dataframe(
                display_forecast,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "Not enough historical data available "
                "for demand forecasting."
            )

    except Exception as e:

        st.error(
            f"Prediction and forecasting error: {e}"
        )

        # ============================================================
# RESOURCE OPTIMIZATION
# ============================================================

elif page == "🛏️ Resource Optimization":

    st.title("🛏️ Resource Optimization")

    st.write(
        "Hospital room and resource utilization overview."
    )

    # --------------------------------------------------------
    # RESOURCE VALUES
    # --------------------------------------------------------

    total_rooms = 100
    available_rooms = 32
    occupied_rooms = 68

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🛏️ Total Rooms",
            total_rooms
        )

    with col2:

        st.metric(
            "🟢 Available Rooms",
            available_rooms
        )

    with col3:

        st.metric(
            "🔴 Occupied Rooms",
            occupied_rooms
        )

    st.markdown("---")

    # --------------------------------------------------------
    # ROOM UTILIZATION CHART
    # --------------------------------------------------------

    st.subheader("📊 Room Utilization")

    import plotly.express as px

    resource_data = pd.DataFrame({
        "Resource": [
            "Available Rooms",
            "Occupied Rooms"
        ],
        "Rooms": [
            available_rooms,
            occupied_rooms
        ]
    })

    resource_fig = px.bar(
        resource_data,
        x="Resource",
        y="Rooms",
        text="Rooms",
        title="Hospital Room Availability"
    )

    resource_fig.update_layout(
        xaxis_title="Room Status",
        yaxis_title="Number of Rooms"
    )

    resource_fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        resource_fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # RESOURCE STATUS
    # --------------------------------------------------------

    st.subheader("🏥 Resource Status")

    resource_table = pd.DataFrame({
        "Resource": [
            "Hospital Rooms"
        ],
        "Total": [
            total_rooms
        ],
        "Available": [
            available_rooms
        ],
        "Occupied": [
            occupied_rooms
        ]
    })

    st.dataframe(
        resource_table,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # INFORMATION
    # --------------------------------------------------------

    st.info(
        "Resource information is currently maintained "
        "using hospital resource values. This module can "
        "later be connected to MySQL for live hospital "
        "resource information."
    )


# ============================================================
# INCIDENT REPORTING
# ============================================================

elif page == "⚠️ Incident Reporting":

    st.title("⚠️ Incident Reporting")

    st.write(
        "Report and store hospital incidents for future review."
    )

    # --------------------------------------------------------
    # INCIDENT FORM
    # --------------------------------------------------------

    with st.form("incident_form"):

        col1, col2 = st.columns(2)

        with col1:

            patient_id = st.text_input(
                "Patient ID",
                placeholder="Example: HP100001"
            )

        with col2:

            incident_type = st.selectbox(
                "Incident Type",
                [
                    "Medical Emergency",
                    "Medication Error",
                    "Fall",
                    "Equipment Failure",
                    "Patient Complaint",
                    "Other"
                ]
            )

        severity = st.selectbox(
            "Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

        description = st.text_area(
            "Incident Description",
            placeholder="Enter incident details..."
        )

        submitted = st.form_submit_button(
            "🚨 Submit Incident",
            use_container_width=True
        )

        if submitted:

            if patient_id.strip() == "":

                st.warning(
                    "Please enter Patient ID."
                )

            elif description.strip() == "":

                st.warning(
                    "Please enter the incident description."
                )

            else:

                try:

                    save_incident(
                        patient_id=patient_id,
                        incident_type=incident_type,
                        severity=severity,
                        description=description,
                        reported_by=st.session_state.username
                    )

                    st.success(
                        "✅ Incident reported successfully."
                    )

                except Exception as e:

                    st.error(
                        f"Unable to save incident: {e}"
                    )

    # --------------------------------------------------------
    # INCIDENT HISTORY
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("📋 Incident History")

    try:

        incidents = get_incidents()

        if incidents is not None:

            if isinstance(incidents, pd.DataFrame):

                if not incidents.empty:

                    st.dataframe(
                        incidents,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No incidents have been reported yet."
                    )

            elif isinstance(incidents, list):

                if len(incidents) > 0:

                    incident_df = pd.DataFrame(
                        incidents
                    )

                    st.dataframe(
                        incident_df,
                        use_container_width=True,
                        hide_index=True
                    )

                else:

                    st.info(
                        "No incidents have been reported yet."
                    )

            else:

                st.info(
                    "No incidents have been reported yet."
                )

        else:

            st.info(
                "No incidents have been reported yet."
            )

    except Exception as e:

        st.warning(
            f"Incident history could not be loaded: {e}"
        )

# ============================================================
# AMBULANCE DISPATCH
# ============================================================
elif page == "🚑 Ambulance Dispatch":

    st.title("🚑 Ambulance Dispatch & Route")

    # -------------------------------------------------
    # SESSION STATE
    # -------------------------------------------------
    if "ambulance_route" not in st.session_state:
        st.session_state.ambulance_route = None

    st.write(
        "Enter the injured patient's current location and "
        "the hospital destination."
    )

    # -------------------------------------------------
    # LOCATION INPUT
    # -------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        patient_location = st.text_input(
            "📍 Patient Location",
            value="MG Road, Bengaluru",
            key="patient_location"
        )

    with col2:
        hospital_location = st.text_input(
            "🏥 Hospital Location",
            value="Bengaluru, Karnataka, India",
            key="hospital_location"
        )

    st.markdown("---")

    # -------------------------------------------------
    # DISPATCH BUTTON
    # -------------------------------------------------
    if st.button(
        "🚑 Dispatch Ambulance",
        type="primary",
        use_container_width=True
    ):

        if not patient_location.strip():
            st.warning("Please enter the patient's location.")

        elif not hospital_location.strip():
            st.warning("Please enter the hospital location.")

        else:

            with st.spinner("📡 Calculating ambulance route..."):

                try:

                    # -----------------------------------------
                    # GEOCODE PATIENT LOCATION
                    # -----------------------------------------
                    patient_result = geocode_address(
                        patient_location
                    )

                    # -----------------------------------------
                    # GEOCODE HOSPITAL LOCATION
                    # -----------------------------------------
                    hospital_result = geocode_address(
                        hospital_location
                    )

                    if patient_result is None:
                        st.error(
                            "❌ Patient location could not be found."
                        )

                    elif hospital_result is None:
                        st.error(
                            "❌ Hospital location could not be found."
                        )

                    else:

                        patient_lat = patient_result[0]
                        patient_lon = patient_result[1]

                        hospital_lat = hospital_result[0]
                        hospital_lon = hospital_result[1]

                        # -----------------------------------------
                        # CALCULATE ROUTE
                        # -----------------------------------------
                        route = get_route(
                            patient_lat,
                            patient_lon,
                            hospital_lat,
                            hospital_lon
                        )

                        if route is None:

                            st.error(
                                "❌ Unable to calculate ambulance route."
                            )

                        else:

                            # -----------------------------------------
                            # SAVE RESULT IN SESSION STATE
                            # -----------------------------------------
                            st.session_state.ambulance_route = {
                                "patient_location": patient_location,
                                "hospital_location": hospital_location,
                                "patient_lat": patient_lat,
                                "patient_lon": patient_lon,
                                "hospital_lat": hospital_lat,
                                "hospital_lon": hospital_lon,
                                "distance_km": route["distance_km"],
                                "duration_min": route["duration_min"],
                                "geometry": route["geometry"]
                            }

                            st.success(
                                "🚑 Ambulance dispatched successfully!"
                            )

                except Exception as e:

                    st.error(
                        f"❌ Route calculation error: {e}"
                    )

    # -------------------------------------------------
    # DISPLAY SAVED ROUTE
    # -------------------------------------------------
    route_data = st.session_state.ambulance_route

    if route_data is not None:

        st.markdown("---")

        st.subheader("🚑 Ambulance Route Status")

        # -----------------------------------------
        # STATUS
        # -----------------------------------------
        st.success(
            "🚑 Ambulance dispatched through the calculated route."
        )

        # -----------------------------------------
        # ROUTE INFORMATION
        # -----------------------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📍 From",
                route_data["patient_location"]
            )

        with col2:
            st.metric(
                "🏥 To",
                route_data["hospital_location"]
            )

        with col3:
            st.metric(
                "📏 Distance",
                f'{route_data["distance_km"]:.2f} km'
            )

        st.info(
            f'⏱️ Estimated Travel Time: '
            f'{route_data["duration_min"]:.0f} minutes'
        )

        # -----------------------------------------
        # MAP
        # -----------------------------------------
        st.subheader("🗺️ Ambulance Route")

        ambulance_map = folium.Map(
            location=[
                route_data["patient_lat"],
                route_data["patient_lon"]
            ],
            zoom_start=13
        )

        # Patient marker
        folium.Marker(
            [
                route_data["patient_lat"],
                route_data["patient_lon"]
            ],
            tooltip="🚑 Patient Pickup Location",
            popup="🚑 Injured Patient",
            icon=folium.Icon(
                color="red",
                icon="plus"
            )
        ).add_to(ambulance_map)

        # Hospital marker
        folium.Marker(
            [
                route_data["hospital_lat"],
                route_data["hospital_lon"]
            ],
            tooltip="🏥 Hospital",
            popup="🏥 Destination Hospital",
            icon=folium.Icon(
                color="blue",
                icon="home"
            )
        ).add_to(ambulance_map)

        # Route line
        folium.GeoJson(
            route_data["geometry"],
            name="Ambulance Route",
            style_function=lambda feature: {
                "color": "red",
                "weight": 7,
                "opacity": 0.8
            }
        ).add_to(ambulance_map)

        st_folium(
            ambulance_map,
            width=None,
            height=550,
            key="ambulance_route_map"
        )

        # -----------------------------------------
        # GOOGLE MAPS NAVIGATION
        # -----------------------------------------
        google_maps_url = (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={route_data['patient_lat']},"
            f"{route_data['patient_lon']}"
            f"&destination={route_data['hospital_lat']},"
            f"{route_data['hospital_lon']}"
            "&travelmode=driving"
        )

        st.markdown(
            f"""
            <a href="{google_maps_url}" target="_blank">
                <button style="
                    width:100%;
                    padding:12px;
                    background:#1976D2;
                    color:white;
                    border:none;
                    border-radius:8px;
                    font-size:16px;
                    cursor:pointer;
                ">
                    🗺️ Open Navigation in Google Maps
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )

elif page == "🔔 Alerts & Notifications":

    st.title("🔔 Alerts & Notifications")
    st.write(
        "Monitor important hospital events, emergencies and system notifications."
    )

    # ---------------------------------------------------------
    # SESSION STATE FOR ALERTS
    # ---------------------------------------------------------

    if "hospital_alerts" not in st.session_state:
        st.session_state.hospital_alerts = []

    # ---------------------------------------------------------
    # AUTOMATIC ALERTS
    # ---------------------------------------------------------

    alerts = []

    # =========================================================
    # 1. EMERGENCY PATIENT ALERT
    # =========================================================

    if "Admission_Type" in df.columns:

        emergency_count = (
            df["Admission_Type"]
            .astype(str)
            .str.lower()
            .eq("emergency")
            .sum()
        )

        if emergency_count > 0:

            alerts.append({
                "type": "Emergency Patient",
                "severity": "Critical",
                "message":
                    f"🚨 {emergency_count} emergency patient(s) "
                    "require immediate attention."
            })

    # =========================================================
    # 2. AMBULANCE ALERT
    # =========================================================

    if (
        "ambulance_route" in st.session_state
        and st.session_state.ambulance_route is not None
    ):

        ambulance = st.session_state.ambulance_route

        alerts.append({
            "type": "Ambulance Dispatch",
            "severity": "Critical",
            "message":
                f"🚑 Ambulance dispatched from "
                f"{ambulance['patient_location']} "
                f"to {ambulance['hospital_location']} "
                f"({ambulance['distance_km']:.2f} km)."
        })

    # =========================================================
    # 3. PENDING PAYMENT ALERT
    # =========================================================

    if "Payment_Status" in df.columns:

        pending_count = (
            df["Payment_Status"]
            .astype(str)
            .str.lower()
            .isin([
                "pending",
                "unpaid",
                "due"
            ])
            .sum()
        )

        if pending_count > 0:

            alerts.append({
                "type": "Payment Alert",
                "severity": "Warning",
                "message":
                    f"💳 {pending_count} patient payment(s) "
                    "are pending."
            })

    # =========================================================
    # 4. CRITICAL INCIDENT ALERTS
    # =========================================================

    for incident in st.session_state.hospital_alerts:

        alerts.append(incident)

    # =========================================================
    # 5. ICU / BED ALERT
    # =========================================================

    # Your current hospital resource values
    total_icu_beds = 20
    available_icu_beds = 5

    if available_icu_beds <= 5:

        alerts.append({
            "type": "ICU Capacity",
            "severity": "Critical",
            "message":
                f"🛏️ Only {available_icu_beds} ICU bed(s) "
                f"are currently available."
        })

    # =========================================================
    # ALERT SUMMARY
    # =========================================================

    critical_alerts = [
        alert
        for alert in alerts
        if alert["severity"] == "Critical"
    ]

    warning_alerts = [
        alert
        for alert in alerts
        if alert["severity"] == "Warning"
    ]

    information_alerts = [
        alert
        for alert in alerts
        if alert["severity"] == "Information"
    ]

    # ---------------------------------------------------------
    # SUMMARY CARDS
    # ---------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🔴 Critical Alerts",
            len(critical_alerts)
        )

    with col2:
        st.metric(
            "🟠 Warnings",
            len(warning_alerts)
        )

    with col3:
        st.metric(
            "🔵 Information",
            len(information_alerts)
        )

    st.markdown("---")

    # =========================================================
    # CRITICAL ALERTS
    # =========================================================

    st.subheader("🔴 Critical Alerts")

    if critical_alerts:

        for alert in critical_alerts:

            st.error(
                f"**{alert['type']}**\n\n"
                f"{alert['message']}"
            )

    else:

        st.success(
            "🟢 No critical alerts at the moment."
        )

    # =========================================================
    # WARNING ALERTS
    # =========================================================

    st.subheader("🟠 Warnings")

    if warning_alerts:

        for alert in warning_alerts:

            st.warning(
                f"**{alert['type']}**\n\n"
                f"{alert['message']}"
            )

    else:

        st.info(
            "No warning notifications."
        )

    # =========================================================
    # INFORMATION
    # =========================================================

    st.subheader("🔵 Information")

    if information_alerts:

        for alert in information_alerts:

            st.info(
                f"**{alert['type']}**\n\n"
                f"{alert['message']}"
            )

    else:

        st.info(
            "No new information notifications."
        )

    # =========================================================
    # DEMO / TEST ALERT
    # =========================================================

    st.markdown("---")

    st.subheader("🧪 Alert Testing")

    if st.button(
        "🚨 Generate Test Critical Alert",
        use_container_width=True
    ):

        st.session_state.hospital_alerts.append({
            "type": "Test Emergency",
            "severity": "Critical",
            "message":
                "🚨 Test critical alert generated successfully. "
                "Hospital staff attention is required."
        })

        st.success(
            "Test critical alert created."
        )

        st.rerun()

    if st.button(
        "🗑️ Clear Test Alerts",
        use_container_width=True
    ):

        st.session_state.hospital_alerts = []

        st.success(
            "Test alerts cleared."
        )

        st.rerun()


# ============================================================
# HISTORY & REPORTS
# ============================================================

elif page == "📄 History & Reports":

    st.title("📄 History & Reports")

    st.download_button(
        label="⬇️ Download Patient Dataset",
        data=df.to_csv(index=False),
        file_name="hospital_patient_report.csv",
        mime="text/csv"
    )

    st.markdown("---")

    st.subheader("Patient Report")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PROFILE & SETTINGS
# ============================================================
elif page == "⚙️ Profile & Settings":

    st.title("⚙️ Profile & Settings")
    st.write("Manage your account, security, notifications and application preferences.")

    # ---------------------------------------------------------
    # INITIALIZE SETTINGS
    # ---------------------------------------------------------

    if "profile_full_name" not in st.session_state:
        st.session_state.profile_full_name = "Hospital Administrator"

    if "profile_email" not in st.session_state:
        st.session_state.profile_email = "admin@hospital.com"

    if "profile_phone" not in st.session_state:
        st.session_state.profile_phone = ""

    if "notification_enabled" not in st.session_state:
        st.session_state.notification_enabled = True

    if "email_alerts" not in st.session_state:
        st.session_state.email_alerts = True

    if "emergency_alerts" not in st.session_state:
        st.session_state.emergency_alerts = True

    if "analytics_enabled" not in st.session_state:
        st.session_state.analytics_enabled = True

    if "auto_refresh" not in st.session_state:
        st.session_state.auto_refresh = False

    if "compact_view" not in st.session_state:
        st.session_state.compact_view = False

    # ---------------------------------------------------------
    # PROFILE HEADER
    # ---------------------------------------------------------

    st.markdown("### 👤 My Profile")

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown(
            """
            <div style="
                background: rgba(255,255,255,0.85);
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                border: 1px solid #dddddd;
            ">
                <div style="font-size:65px;">👨‍⚕️</div>
                <h3>Hospital Administrator</h3>
                <p>System Administrator</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown("#### Account Information")

        st.write(
            f"**Username:** {st.session_state.username}"
        )

        st.write(
            f"**Role:** Hospital Administrator"
        )

        st.write(
            f"**Patient Records:** {len(df):,}"
        )

        st.write(
            f"**Departments:** {df['Department'].nunique()}"
        )

        st.success("🟢 Account Status: Active")

    st.markdown("---")

    # ---------------------------------------------------------
    # TABS
    # ---------------------------------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "👤 Personal Information",
            "🔐 Security",
            "🔔 Notifications",
            "🎨 Application Settings",
            "ℹ️ System Information"
        ]
    )

    # =========================================================
    # TAB 1 - PERSONAL INFORMATION
    # =========================================================

    with tab1:

        st.subheader("👤 Personal Information")

        with st.form("personal_information_form"):

            full_name = st.text_input(
                "Full Name",
                value=st.session_state.profile_full_name
            )

            email = st.text_input(
                "Email Address",
                value=st.session_state.profile_email
            )

            phone = st.text_input(
                "Phone Number",
                value=st.session_state.profile_phone
            )

            role = st.selectbox(
                "Role",
                [
                    "Hospital Administrator",
                    "Doctor",
                    "Nurse",
                    "Receptionist",
                    "Data Analyst",
                    "Staff"
                ],
                index=0
            )

            save_profile = st.form_submit_button(
                "💾 Save Profile",
                use_container_width=True
            )

            if save_profile:

                if full_name.strip() == "":
                    st.warning("Please enter your full name.")

                elif email.strip() == "":
                    st.warning("Please enter your email address.")

                else:

                    st.session_state.profile_full_name = full_name
                    st.session_state.profile_email = email
                    st.session_state.profile_phone = phone

                    st.success(
                        "✅ Profile information updated successfully."
                    )

    # =========================================================
    # TAB 2 - SECURITY
    # =========================================================

    with tab2:

        st.subheader("🔐 Account Security")

        st.info(
            "Change your username or password from this section."
        )

        with st.form("security_form"):

            current_username = st.text_input(
                "Current Username",
                value=st.session_state.username,
                disabled=True
            )

            new_username = st.text_input(
                "New Username",
                placeholder="Enter new username"
            )

            st.markdown("### 🔑 Change Password")

            current_password = st.text_input(
                "Current Password",
                type="password"
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Enter new password"
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
                placeholder="Re-enter new password"
            )

            change_account = st.form_submit_button(
                "🔐 Update Account",
                use_container_width=True
            )

            if change_account:

                username_changed = False
                password_changed = False

                # ---------------------------------------------
                # CHANGE USERNAME
                # ---------------------------------------------

                if new_username.strip():

                    if new_username.strip() == st.session_state.username:

                        st.warning(
                            "New username is same as current username."
                        )

                    elif new_username.strip() in st.session_state.users:

                        st.error(
                            "❌ Username already exists."
                        )

                    else:

                        old_username = st.session_state.username

                        old_password = st.session_state.users[
                            old_username
                        ]

                        st.session_state.users[
                            new_username.strip()
                        ] = old_password

                        del st.session_state.users[
                            old_username
                        ]

                        st.session_state.username = (
                            new_username.strip()
                        )

                        username_changed = True

                # ---------------------------------------------
                # CHANGE PASSWORD
                # ---------------------------------------------

                if new_password or confirm_password:

                    old_username = st.session_state.username

                    stored_password = st.session_state.users.get(
                        old_username,
                        ""
                    )

                    if current_password != stored_password:

                        st.error(
                            "❌ Current password is incorrect."
                        )

                    elif new_password != confirm_password:

                        st.error(
                            "❌ New passwords do not match."
                        )

                    elif len(new_password) < 6:

                        st.error(
                            "❌ Password must contain at least 6 characters."
                        )

                    else:

                        st.session_state.users[
                            old_username
                        ] = new_password

                        password_changed = True

                # ---------------------------------------------
                # SUCCESS MESSAGE
                # ---------------------------------------------

                if username_changed and password_changed:

                    st.success(
                        "✅ Username and password updated successfully."
                    )

                elif username_changed:

                    st.success(
                        "✅ Username updated successfully."
                    )

                elif password_changed:

                    st.success(
                        "✅ Password updated successfully."
                    )

    # =========================================================
    # TAB 3 - NOTIFICATIONS
    # =========================================================

    with tab3:

        st.subheader("🔔 Notification Settings")

        st.session_state.notification_enabled = st.toggle(
            "Enable Notifications",
            value=st.session_state.notification_enabled,
            key="notification_toggle"
        )

        st.session_state.emergency_alerts = st.toggle(
            "🚑 Emergency / Ambulance Alerts",
            value=st.session_state.emergency_alerts,
            key="emergency_toggle"
        )

        st.session_state.email_alerts = st.toggle(
            "📧 Email Notifications",
            value=st.session_state.email_alerts,
            key="email_toggle"
        )

        st.markdown("### Notification Types")

        col1, col2 = st.columns(2)

        with col1:

            st.checkbox(
                "⚠️ Critical Patient Alerts",
                value=True,
                key="critical_alerts"
            )

            st.checkbox(
                "🛏️ Bed Availability Alerts",
                value=True,
                key="bed_alerts"
            )

        with col2:

            st.checkbox(
                "💊 Medication Alerts",
                value=True,
                key="medication_alerts"
            )

            st.checkbox(
                "📅 Appointment Reminders",
                value=True,
                key="appointment_alerts"
            )

        st.success("🔔 Notification preferences are active.")

    # =========================================================
    # TAB 4 - APPLICATION SETTINGS
    # =========================================================

    with tab4:

        st.subheader("🎨 Application Settings")

        st.markdown("### Dashboard Preferences")

        st.session_state.analytics_enabled = st.toggle(
            "📊 Show Analytics",
            value=st.session_state.analytics_enabled,
            key="analytics_toggle"
        )

        st.session_state.auto_refresh = st.toggle(
            "🔄 Enable Auto Refresh",
            value=st.session_state.auto_refresh,
            key="refresh_toggle"
        )

        st.session_state.compact_view = st.toggle(
            "📱 Compact Dashboard View",
            value=st.session_state.compact_view,
            key="compact_toggle"
        )

        st.markdown("### 📊 Dashboard Display")

        dashboard_default = st.selectbox(
            "Default Dashboard View",
            [
                "Overview",
                "Patient Analytics",
                "Financial Overview",
                "Resource Overview"
            ]
        )

        records_per_page = st.selectbox(
            "Patient Records per Page",
            [
                10,
                25,
                50,
                100
            ]
        )

        date_format = st.selectbox(
            "Date Format",
            [
                "DD-MM-YYYY",
                "DD/MM/YYYY",
                "YYYY-MM-DD"
            ]
        )

        st.markdown("### 🌐 System Preferences")

        language = st.selectbox(
            "Language",
            [
                "English"
            ]
        )

        timezone = st.selectbox(
            "Time Zone",
            [
                "India Standard Time (IST)",
                "UTC",
                "GMT"
            ]
        )

        st.success(
            "⚙️ Application preferences saved for this session."
        )

    # =========================================================
    # TAB 5 - SYSTEM INFORMATION
    # =========================================================

    with tab5:

        st.subheader("ℹ️ System Information")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🏥 Hospital System")

            st.write("**System:** Hospital Patient Management System")
            st.write("**Version:** 1.0")
            st.write("**Platform:** Streamlit")
            st.write("**Database:** MySQL / SQLite")
            st.write("**Analytics:** Python + Pandas + Plotly")
            st.write("**Prediction:** Machine Learning")

        with col2:

            st.markdown("### 📊 System Statistics")

            st.metric(
                "Total Patients",
                f"{len(df):,}"
            )

            st.metric(
                "Departments",
                df["Department"].nunique()
            )

            st.metric(
                "Doctors",
                df["Doctor"].nunique()
            )

            st.metric(
                "Patient Diagnoses",
                df["Diagnosis"].nunique()
            )

        st.markdown("---")

        st.info(
            "🔒 Your account settings are managed by the "
            "Hospital Management System."
        )

    # ---------------------------------------------------------
    # ACCOUNT ACTIONS
    # ---------------------------------------------------------

    st.markdown("---")

    st.subheader("🚨 Account Actions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔄 Reset Application Settings",
            use_container_width=True
        ):

            st.session_state.notification_enabled = True
            st.session_state.email_alerts = True
            st.session_state.emergency_alerts = True
            st.session_state.analytics_enabled = True
            st.session_state.auto_refresh = False
            st.session_state.compact_view = False

            st.success(
                "✅ Application settings reset successfully."
            )

    with col2:

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.success("Logged out successfully.")

            st.rerun()