# 🏥 Hospital Patient Management System

A Streamlit-based Hospital Patient Management System for patient records, analytics, prediction, resource optimization, incident reporting, alerts, and reports.

## Project Structure

```text
Hospital Patient Management System/
│
├── data/
│   └── hospital_patient.csv
├── images/
│   └── hospital_background.png
├── MYSQL/
│   └── database.py
├── src/
│   ├── database.py
│   ├── data_processing.py
│   ├── analytics.py
│   ├── prediction.py
│   └── optimization.py
├── Graphs.py
├── app.py
├── hospital_management.db
└── README.md
```

## Technologies

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn
- MySQL
- SQLite
- VS Code

## Main Modules

1. Dashboard
2. Patient Records
3. Patient Analytics
4. Prediction & Forecasting
5. Resource Optimization
6. Incident Reporting
7. Alerts & Notifications
8. History & Reports
9. Profile & Settings
10. Login / Sign Up / Forgot Password

## Database

Main application database:

```text
hospital_management_db
```

The included `hospital_management.db` is a SQLite database for local viewing/testing in VS Code with a SQLite Viewer extension. It does not replace the MySQL database used by the application.

### SQLite Tables

- Users
- Patients
- Appointments
- Incidents
- Alerts
- Hospital_Resources

### Default Login

```text
Username: admin
Password: admin123
```

## Run the Application

Open the project folder in VS Code and run:

```bash
streamlit run app.py
```

## Install Packages

```bash
python -m pip install streamlit pandas plotly scikit-learn mysql-connector-python
```

## MySQL Configuration

```text
Host: localhost
User: root
Database: hospital_management_db
```

Update the MySQL password in `MYSQL/database.py` to match your local MySQL installation.

## Analytics

The application includes:

- Yearly Patient Trend
- Monthly Patient Trend
- Department Graph
- Admission Type
- Payment Status
- Patient Status
- Yearly Revenue

## Important Note

The SQLite file is provided mainly so the database can be opened and viewed in VS Code like the database shown in the screenshot. For the Streamlit application, continue using MySQL as the main database unless you intentionally change the application to SQLite.

For a real production system, passwords should be securely hashed rather than stored as plain text.
