import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
# Get src folder path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from data_processing import get_clean_data


# =========================================================
# ANALYTICS FUNCTIONS
# =========================================================

def total_patients(df):
    return df["Patient_ID"].nunique()


def total_revenue(df):
    return df["Total_Bill"].sum()


def average_bill(df):
    return df["Total_Bill"].mean()


def average_age(df):
    return df["Age"].mean()


def department_statistics(df):
    return (
        df.groupby("Department")
        .agg(
            Patients=("Patient_ID", "count"),
            Revenue=("Total_Bill", "sum"),
            Average_Bill=("Total_Bill", "mean")
        )
        .reset_index()
        .sort_values("Patients", ascending=False)
    )


def admission_type_statistics(df):
    result = df["Admission_Type"].value_counts().reset_index()
    result.columns = ["Admission_Type", "Patient_Count"]
    return result


def gender_statistics(df):
    result = df["Gender"].value_counts().reset_index()
    result.columns = ["Gender", "Patient_Count"]
    return result


def payment_statistics(df):
    result = df["Payment_Status"].value_counts().reset_index()
    result.columns = ["Payment_Status", "Patient_Count"]
    return result


def patient_status_statistics(df):
    result = df["Patient_Status"].value_counts().reset_index()
    result.columns = ["Patient_Status", "Patient_Count"]
    return result


def yearly_statistics(df):
    return (
        df.groupby("Admission_Year")
        .agg(
            Patients=("Patient_ID", "count"),
            Revenue=("Total_Bill", "sum")
        )
        .reset_index()
        .sort_values("Admission_Year")
    )


# =========================================================
# RUN ANALYTICS
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("       HOSPITAL PATIENT MANAGEMENT SYSTEM")
    print("                 ANALYTICS MODULE")
    print("=" * 70)

    # Load dataset
    df = get_clean_data()

    print("\nDataset loaded successfully!")
    print("Total records:", len(df))

    # =====================================================
    # 1 BASIC SUMMARY
    # =====================================================

    print("\n")
    print("-" * 70)
    print("1. BASIC HOSPITAL SUMMARY")
    print("-" * 70)

    print("Total Patients :", total_patients(df))
    print("Total Revenue  :", round(total_revenue(df), 2))
    print("Average Bill   :", round(average_bill(df), 2))
    print("Average Age    :", round(average_age(df), 2))

    # =====================================================
    # 2 DEPARTMENT
    # =====================================================

    print("\n")
    print("-" * 70)
    print("2. DEPARTMENT STATISTICS")
    print("-" * 70)

    print(
        department_statistics(df).to_string(index=False)
    )

    # =====================================================
    # 3 ADMISSION TYPE
    # =====================================================

    print("\n")
    print("-" * 70)
    print("3. ADMISSION TYPE")
    print("-" * 70)

    print(
        admission_type_statistics(df).to_string(index=False)
    )

    # =====================================================
    # 4 GENDER
    # =====================================================

    print("\n")
    print("-" * 70)
    print("4. GENDER STATISTICS")
    print("-" * 70)

    print(
        gender_statistics(df).to_string(index=False)
    )

    # =====================================================
    # 5 PAYMENT
    # =====================================================

    print("\n")
    print("-" * 70)
    print("5. PAYMENT STATUS")
    print("-" * 70)

    print(
        payment_statistics(df).to_string(index=False)
    )

    # =====================================================
    # 6 PATIENT STATUS
    # =====================================================

    print("\n")
    print("-" * 70)
    print("6. PATIENT STATUS")
    print("-" * 70)

    print(
        patient_status_statistics(df).to_string(index=False)
    )

    # =====================================================
    # 7 YEARLY ANALYSIS
    # =====================================================

    print("\n")
    print("-" * 70)
    print("7. YEARLY PATIENT ANALYSIS")
    print("-" * 70)

    print(
        yearly_statistics(df).to_string(index=False)
    )

    # =====================================================
    # FINISH
    # =====================================================

    print("\n")
    print("=" * 70)
    print("             ANALYTICS COMPLETED")
    print("=" * 70)