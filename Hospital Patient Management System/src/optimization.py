import sys
import os
import pandas as pd

# Add src folder to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from data_processing import get_clean_data


# =========================================================
# 1. DEPARTMENT LOAD
# =========================================================

def department_load(df):

    result = (
        df.groupby("Department")
        .agg(
            Total_Patients=("Patient_ID", "count"),
            Under_Treatment=(
                "Patient_Status",
                lambda x: (x == "Under Treatment").sum()
            ),
            Average_Age=("Age", "mean"),
            Total_Revenue=("Total_Bill", "sum")
        )
        .reset_index()
    )

    return result.sort_values(
        "Total_Patients",
        ascending=False
    )


# =========================================================
# 2. ADMISSION LOAD
# =========================================================

def admission_load(df):

    result = (
        df.groupby("Admission_Type")
        .agg(
            Patient_Count=("Patient_ID", "count")
        )
        .reset_index()
    )

    return result.sort_values(
        "Patient_Count",
        ascending=False
    )


# =========================================================
# 3. ROOM OCCUPANCY
# =========================================================

def room_occupancy(df):

    result = (
        df.groupby("Room_No")
        .agg(
            Patient_Count=("Patient_ID", "count"),
            Current_Status=("Patient_Status", "last")
        )
        .reset_index()
    )

    return result


# =========================================================
# 4. HIGH LOAD DEPARTMENTS
# =========================================================

def high_load_departments(df, threshold=100):

    department_data = department_load(df)

    return department_data[
        department_data["Total_Patients"] >= threshold
    ]


# =========================================================
# 5. PENDING PAYMENTS
# =========================================================

def payment_pending_patients(df):

    return df[
        df["Payment_Status"].isin(
            ["Pending", "Partial"]
        )
    ][
        [
            "Patient_ID",
            "Patient_Name",
            "Department",
            "Total_Bill",
            "Payment_Status"
        ]
    ]


# =========================================================
# 6. PATIENT STATUS LOAD
# =========================================================

def patient_status_load(df):

    result = (
        df.groupby("Patient_Status")
        .agg(
            Patient_Count=("Patient_ID", "count")
        )
        .reset_index()
    )

    return result.sort_values(
        "Patient_Count",
        ascending=False
    )


# =========================================================
# 7. DEPARTMENT RESOURCE REQUIREMENT
# =========================================================

def resource_requirement(df):

    result = (
        df.groupby("Department")
        .agg(
            Patients=("Patient_ID", "count"),
            Under_Treatment=(
                "Patient_Status",
                lambda x: (x == "Under Treatment").sum()
            ),
            Emergency_Cases=(
                "Admission_Type",
                lambda x: (x == "Emergency").sum()
            )
        )
        .reset_index()
    )

    # Simple resource level
    def resource_level(row):

        if row["Patients"] >= 500:
            return "Very High"

        elif row["Patients"] >= 300:
            return "High"

        elif row["Patients"] >= 150:
            return "Medium"

        else:
            return "Low"

    result["Resource_Level"] = result.apply(
        resource_level,
        axis=1
    )

    return result.sort_values(
        "Patients",
        ascending=False
    )


# =========================================================
# RUN OPTIMIZATION MODULE
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("       HOSPITAL PATIENT MANAGEMENT SYSTEM")
    print("              OPTIMIZATION MODULE")
    print("=" * 70)

    try:

        # Load dataset
        df = get_clean_data()

        print("\nDataset loaded successfully!")
        print("Total records:", len(df))

        # =================================================
        # 1 DEPARTMENT LOAD
        # =================================================

        print("\n")
        print("-" * 70)
        print("1. DEPARTMENT LOAD")
        print("-" * 70)

        print(
            department_load(df)
            .to_string(index=False)
        )

        # =================================================
        # 2 ADMISSION LOAD
        # =================================================

        print("\n")
        print("-" * 70)
        print("2. ADMISSION LOAD")
        print("-" * 70)

        print(
            admission_load(df)
            .to_string(index=False)
        )

        # =================================================
        # 3 ROOM OCCUPANCY
        # =================================================

        print("\n")
        print("-" * 70)
        print("3. ROOM OCCUPANCY")
        print("-" * 70)

        print(
            room_occupancy(df)
            .head(20)
            .to_string(index=False)
        )

        print("\nShowing first 20 rooms...")

        # =================================================
        # 4 HIGH LOAD DEPARTMENTS
        # =================================================

        print("\n")
        print("-" * 70)
        print("4. HIGH LOAD DEPARTMENTS")
        print("-" * 70)

        high_load = high_load_departments(
            df,
            threshold=100
        )

        if len(high_load) > 0:

            print(
                high_load
                .to_string(index=False)
            )

        else:

            print("No department crossed the threshold.")

        # =================================================
        # 5 PENDING / PARTIAL PAYMENTS
        # =================================================

        print("\n")
        print("-" * 70)
        print("5. PENDING / PARTIAL PAYMENTS")
        print("-" * 70)

        pending = payment_pending_patients(df)

        print(
            pending
            .head(20)
            .to_string(index=False)
        )

        print(
            "\nTotal pending/partial payment patients:",
            len(pending)
        )

        # =================================================
        # 6 PATIENT STATUS
        # =================================================

        print("\n")
        print("-" * 70)
        print("6. PATIENT STATUS LOAD")
        print("-" * 70)

        print(
            patient_status_load(df)
            .to_string(index=False)
        )

        # =================================================
        # 7 RESOURCE REQUIREMENT
        # =================================================

        print("\n")
        print("-" * 70)
        print("7. RESOURCE REQUIREMENT")
        print("-" * 70)

        print(
            resource_requirement(df)
            .to_string(index=False)
        )

        # =================================================
        # COMPLETED
        # =================================================

        print("\n")
        print("=" * 70)
        print("          OPTIMIZATION COMPLETED")
        print("=" * 70)

    except Exception as e:

        print("\n")
        print("=" * 70)
        print("ERROR IN OPTIMIZATION MODULE")
        print("=" * 70)

        print(e)

        print("\nPlease check:")
        print("1. hospital_patient.csv is inside data folder")
        print("2. data_processing.py is inside src folder")
        print("3. Column names match the dataset")