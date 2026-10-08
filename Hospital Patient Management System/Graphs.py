import pandas as pd
import plotly.express as px


def prepare_data(df):
    data = df.copy()

    data["Admission_Date"] = pd.to_datetime(
        data["Admission_Date"],
        errors="coerce"
    )

    data["Admission_Year"] = data["Admission_Date"].dt.year

    data["Month_Year"] = (
        data["Admission_Date"]
        .dt.to_period("M")
        .astype(str)
    )

    return data


# ============================================================
# 1. YEARLY PATIENT TREND
# ============================================================

def yearly_patient_trend(df):

    data = prepare_data(df)

    result = (
        data.groupby("Admission_Year")
        .size()
        .reset_index(name="Patients")
    )

    fig = px.line(
        result,
        x="Admission_Year",
        y="Patients",
        markers=True,
        title="Yearly Patient Trend"
    )

    return fig


# ============================================================
# 2. MONTHLY PATIENT TREND
# ============================================================

def monthly_patient_trend(df):

    data = prepare_data(df)

    result = (
        data.groupby("Month_Year")
        .size()
        .reset_index(name="Patients")
    )

    fig = px.line(
        result,
        x="Month_Year",
        y="Patients",
        markers=True,
        title="Monthly Patient Trend"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Patients"
    )

    return fig


# ============================================================
# 3. DEPARTMENT GRAPH
# ============================================================

def department_graph(df):

    result = (
        df["Department"]
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "Department",
        "Patients"
    ]

    fig = px.bar(
        result,
        x="Department",
        y="Patients",
        title="Patients by Department"
    )

    return fig


# ============================================================
# 4. ADMISSION TYPE
# ============================================================

def admission_type_graph(df):

    result = (
        df["Admission_Type"]
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "Admission_Type",
        "Patients"
    ]

    fig = px.bar(
        result,
        x="Admission_Type",
        y="Patients",
        title="Patients by Admission Type"
    )

    return fig


# ============================================================
# 5. PAYMENT STATUS
# ============================================================

def payment_status_graph(df):

    result = (
        df["Payment_Status"]
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "Payment_Status",
        "Patients"
    ]

    fig = px.pie(
        result,
        names="Payment_Status",
        values="Patients",
        title="Payment Status"
    )

    return fig


# ============================================================
# 6. PATIENT STATUS
# ============================================================

def patient_status_graph(df):

    result = (
        df["Patient_Status"]
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "Patient_Status",
        "Patients"
    ]

    fig = px.pie(
        result,
        names="Patient_Status",
        values="Patients",
        title="Patient Status"
    )

    return fig


# ============================================================
# 7. YEARLY REVENUE
# ============================================================

def yearly_revenue_graph(df):

    data = prepare_data(df)

    data["Total_Bill"] = pd.to_numeric(
        data["Total_Bill"],
        errors="coerce"
    )

    result = (
        data.groupby("Admission_Year")["Total_Bill"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        result,
        x="Admission_Year",
        y="Total_Bill",
        title="Yearly Revenue"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Revenue (₹)"
    )

    return fig