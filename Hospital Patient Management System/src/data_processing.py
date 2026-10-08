import pandas as pd
import os


# Get project folder
PROJECT_FOLDER = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# CSV location
DATA_PATH = os.path.join(
    PROJECT_FOLDER,
    "data",
    "hospital_patient.csv"
)


def load_data():

    print("\nChecking dataset path...")
    print("Dataset path:", DATA_PATH)

    if not os.path.exists(DATA_PATH):
        print("\n❌ ERROR: hospital_patient.csv not found!")
        print("Make sure the file is inside the data folder.")
        return pd.DataFrame()

    print("\n✅ Dataset found!")

    try:
        df = pd.read_csv(DATA_PATH)

        print("✅ Dataset loaded successfully!")
        print("Total rows:", len(df))
        print("Total columns:", len(df.columns))

        return df

    except Exception as e:

        print("\n❌ Error while reading CSV:")
        print(e)

        return pd.DataFrame()


def clean_data(df):

    if df.empty:
        return df

    df = df.copy()

    print("\nCleaning dataset...")

    # Convert Admission Date
    if "Admission_Date" in df.columns:

        df["Admission_Date"] = pd.to_datetime(
            df["Admission_Date"],
            dayfirst=True,
            errors="coerce"
        )

    # Convert Discharge Date
    if "Discharge_Date" in df.columns:

        df["Discharge_Date"] = pd.to_datetime(
            df["Discharge_Date"],
            dayfirst=True,
            errors="coerce"
        )

    # Convert Age
    if "Age" in df.columns:

        df["Age"] = pd.to_numeric(
            df["Age"],
            errors="coerce"
        )

    # Convert Total Bill
    if "Total_Bill" in df.columns:

        df["Total_Bill"] = pd.to_numeric(
            df["Total_Bill"],
            errors="coerce"
        )

    # Create Admission Year
    if "Admission_Date" in df.columns:

        df["Admission_Year"] = (
            df["Admission_Date"].dt.year
        )

        # Create month number
        df["Admission_Month"] = (
            df["Admission_Date"].dt.month
        )

        # Create month name
        df["Month_Name"] = (
            df["Admission_Date"].dt.strftime("%B")
        )

        # Create Month-Year
        df["Month_Year"] = (
            df["Admission_Date"].dt.strftime("%b %Y")
        )

    # Calculate Length of Stay
    if (
        "Admission_Date" in df.columns
        and "Discharge_Date" in df.columns
    ):

        df["Length_of_Stay"] = (
            df["Discharge_Date"]
            - df["Admission_Date"]
        ).dt.days

        df["Length_of_Stay"] = (
            df["Length_of_Stay"].fillna(0)
        )

    # Age Group
    if "Age" in df.columns:

        def age_group(age):

            if pd.isna(age):
                return "Unknown"

            if age <= 12:
                return "Child"

            elif age <= 19:
                return "Teenager"

            elif age <= 39:
                return "Young Adult"

            elif age <= 59:
                return "Middle Age"

            else:
                return "Senior Citizen"

        df["Age_Group"] = df["Age"].apply(age_group)

    print("✅ Data cleaning completed!")

    return df


def get_clean_data():

    df = load_data()

    if df.empty:
        return df

    df = clean_data(df)

    return df


# ------------------------------------------------
# TEST THE FILE
# ------------------------------------------------

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("   HOSPITAL PATIENT DATA PROCESSING")
    print("=" * 60)

    df = get_clean_data()

    if df.empty:

        print("\n❌ No data available.")
        print("Please check your CSV file.")

    else:

        print("\n" + "=" * 60)
        print("DATASET INFORMATION")
        print("=" * 60)

        print("\nRows:", len(df))
        print("Columns:", len(df.columns))

        print("\nColumn Names:")

        for column in df.columns:
            print(" -", column)

        print("\n" + "=" * 60)
        print("FIRST 5 RECORDS")
        print("=" * 60)

        print(df.head().to_string(index=False))

        print("\n" + "=" * 60)
        print("DATA TYPES")
        print("=" * 60)

        print(df.dtypes)

        print("\n" + "=" * 60)
        print("MISSING VALUES")
        print("=" * 60)

        print(df.isnull().sum())

        print("\n" + "=" * 60)
        print("DATA PROCESSING COMPLETED")
        print("=" * 60)