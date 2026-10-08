import sqlite3
import os


# ============================================================
# DATABASE PATH
# ============================================================

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(
    PROJECT_DIR,
    "hospital_management.db"
)


# ============================================================
# CREATE DATABASE AND TABLE
# ============================================================

def create_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id TEXT,

            incident_type TEXT,

            severity TEXT,

            description TEXT,

            reported_by TEXT,

            incident_date TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# SAVE INCIDENT
# ============================================================

def save_incident(
    patient_id,
    incident_type,
    severity,
    description,
    reported_by
):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO incidents
        (
            patient_id,
            incident_type,
            severity,
            description,
            reported_by
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        patient_id,
        incident_type,
        severity,
        description,
        reported_by
    ))

    connection.commit()

    connection.close()


# ============================================================
# GET ALL INCIDENTS
# ============================================================

def get_incidents():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            patient_id,
            incident_type,
            severity,
            description,
            reported_by,
            incident_date
        FROM incidents
        ORDER BY id DESC
    """)

    incidents = cursor.fetchall()

    connection.close()

    return incidents


# ============================================================
# TEST DATABASE
# ============================================================

if __name__ == "__main__":

    create_database()

    print("================================================")
    print("   HOSPITAL SQLITE DATABASE")
    print("================================================")

    print("\nDatabase created successfully.")

    print(
        "\nDatabase Location:",
        DATABASE_PATH
    )

    incidents = get_incidents()

    print(
        "\nTotal Incidents:",
        len(incidents)
    )

    print("================================================")