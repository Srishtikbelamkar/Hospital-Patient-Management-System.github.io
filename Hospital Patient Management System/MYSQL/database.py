import mysql.connector
from mysql.connector import Error


# ============================================================
# MYSQL DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "hospital_management_db"
}


# ============================================================
# CREATE DATABASE CONNECTION
# ============================================================

def create_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        if connection.is_connected():

            print("SUCCESS!")
            print("MySQL connected successfully.")
            print("Database:", DB_CONFIG["database"])

            return connection

    except Error as e:

        print("MySQL connection failed.")
        print("Error:", e)

    return None


# ============================================================
# CLOSE DATABASE CONNECTION
# ============================================================

def close_connection(connection):

    if connection is not None:

        if connection.is_connected():

            connection.close()

            print("MySQL connection closed.")


# ============================================================
# SHOW DATABASE TABLES
# ============================================================

def show_tables():

    connection = create_connection()

    if connection:

        cursor = connection.cursor()

        print("\n--- DATABASE TABLES ---")

        cursor.execute("SHOW TABLES")

        tables = cursor.fetchall()

        for table in tables:
            print("✓", table[0])

        cursor.close()

        close_connection(connection)


# ============================================================
# SHOW USERS
# ============================================================

def show_users():

    connection = create_connection()

    if connection:

        cursor = connection.cursor()

        print("\n--- USERS ---")

        cursor.execute("""
            SELECT User_ID, Username, Full_Name, Email
            FROM Users
        """)

        users = cursor.fetchall()

        for user in users:
            print(user)

        cursor.close()

        close_connection(connection)


# ============================================================
# SHOW PATIENT INFORMATION
# ============================================================

def show_patient_information():

    connection = create_connection()

    if connection:

        cursor = connection.cursor()

        print("\n--- PATIENT INFORMATION ---")

        # TOTAL PATIENTS
        cursor.execute(
            "SELECT COUNT(*) FROM Patients"
        )

        patient_count = cursor.fetchone()[0]

        print("Total Patients:", patient_count)

        # TOTAL DEPARTMENTS
        cursor.execute(
            "SELECT COUNT(DISTINCT Department) FROM Patients"
        )

        department_count = cursor.fetchone()[0]

        print("Total Departments:", department_count)

        # TOTAL REVENUE
        cursor.execute(
            "SELECT COALESCE(SUM(Total_Bill), 0) FROM Patients"
        )

        total_revenue = cursor.fetchone()[0]

        print("Total Hospital Revenue: ₹", total_revenue)

        cursor.close()

        close_connection(connection)


# ============================================================
# SHOW PATIENT STATUS
# ============================================================

def show_patient_status():

    connection = create_connection()

    if connection:

        cursor = connection.cursor()

        print("\n--- PATIENT STATUS ---")

        cursor.execute("""
            SELECT Patient_Status, COUNT(*)
            FROM Patients
            GROUP BY Patient_Status
        """)

        statuses = cursor.fetchall()

        for status in statuses:
            print(status[0], ":", status[1])

        cursor.close()

        close_connection(connection)


# ============================================================
# SHOW DEPARTMENT-WISE PATIENTS
# ============================================================

def show_department_patients():

    connection = create_connection()

    if connection:

        cursor = connection.cursor()

        print("\n--- DEPARTMENT-WISE PATIENTS ---")

        cursor.execute("""
            SELECT Department, COUNT(*)
            FROM Patients
            GROUP BY Department
            ORDER BY Department
        """)

        departments = cursor.fetchall()

        for department in departments:
            print(department[0], ":", department[1])

        cursor.close()

        close_connection(connection)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n=======================================================")
    print("   HOSPITAL PATIENT MANAGEMENT SYSTEM")
    print("=======================================================")

    # TEST CONNECTION
    connection = create_connection()

    if connection:

        cursor = connection.cursor()

        cursor.execute("SELECT DATABASE()")

        result = cursor.fetchone()

        print("\nConnected database:", result[0])

        cursor.close()

        close_connection(connection)

        # SHOW TABLES
        show_tables()

        # SHOW USERS
        show_users()

        # SHOW PATIENT INFORMATION
        show_patient_information()

        # SHOW PATIENT STATUS
        show_patient_status()

        # SHOW DEPARTMENT-WISE PATIENTS
        show_department_patients()

    print("\n=======================================================")
    print("   DATABASE TEST COMPLETED")
    print("=======================================================")