import streamlit as st
import mysql.connector
from mysql.connector import Error, IntegrityError
import pandas as pd

# Define database connection parameters
db_params = {
    'host': 'userdata.czgqi48oamxp.eu-north-1.rds.amazonaws.com',
    'database': 'userdata',
    'user': 'admin',
    'password': 'IITJdb123'
}

def connect():
    """Create a database connection."""
    conn = None
    try:
        conn = mysql.connector.connect(**db_params)
        if conn.is_connected():
            return conn
        else:
            st.error("Failed to connect to the database.")
    except Error as e:
        st.error(f"Error: {e}")
    return conn

def insert_data(name, age, medical_history, created_at, gender):
    """Insert a new patient record into the table."""
    conn = connect()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        query = """
            INSERT INTO patientdetails (name, age, medical_history, created_at, gender)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (name, age, medical_history, created_at, gender))
            conn.commit()
            st.success("Data inserted successfully")
        except IntegrityError as e:
            st.error(f"IntegrityError: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        st.error("Failed to insert data. Database connection is not available.")

def get_all_data():
    """Retrieve all patient records from the table."""
    conn = connect()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patientdetails")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    else:
        st.error("Failed to retrieve data. Database connection is not available.")
        return []

def get_patient_data(patient_id):
    """Retrieve data for a specific patient by ID."""
    conn = connect()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patientdetails WHERE id = %s", (patient_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    else:
        st.error("Failed to retrieve data. Database connection is not available.")
        return None

def update_data(id, name=None, age=None, medical_history=None, gender=None):
    """Update a patient record."""
    conn = connect()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        query = "UPDATE patientdetails SET "
        params = []
        if name:
            query += "name = %s, "
            params.append(name)
        if age:
            query += "age = %s, "
            params.append(age)
        if medical_history:
            query += "medical_history = %s, "
            params.append(medical_history)
        if gender:
            query += "gender = %s, "
            params.append(gender)
        query = query.rstrip(', ')  # Remove the last comma
        query += " WHERE id = %s"
        params.append(id)
        cursor.execute(query, tuple(params))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Data updated successfully")
    else:
        st.error("Failed to update data. Database connection is not available.")

def delete_data(id):
    """Delete a patient record."""
    conn = connect()
    if conn and conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patientdetails WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Data deleted successfully")
    else:
        st.error("Failed to delete data. Database connection is not available.")

# Streamlit app
#logo_url = "path_to_your_logo.png"  # Replace with the path to your logo file

# Define fixed login credentials
USERNAME = "admin"
PASSWORD = "IITJ"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    """Handle login."""
    #st.image(logo_url, width=100)  # Adjust width as needed
    st.title("Hospital Patient Details Management System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful")
        else:
            st.error("Invalid username or password")

if not st.session_state.logged_in:
    login()
else:
    #st.image(logo_url, width=100)  # Adjust width as needed
    st.title("Hospital Patient Details Management System")

    menu = ["Insert", "View All", "View by ID", "Update", "Delete", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Insert":
        st.subheader("Insert Data")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        medical_history = st.text_area("Medical History")
        created_at = st.date_input("Created At")
        gender = st.selectbox("Gender", ["M", "F", "Other"])
        
        if st.button("Insert"):
            insert_data(name, age, medical_history, created_at, gender)

    elif choice == "View All":
        st.subheader("View All Data")
        data = get_all_data()
        if data:
            df = pd.DataFrame(data, columns=["ID", "Name", "Age", "Medical History", "Created At", "Gender"])
            st.table(df.style.hide(axis=0))
        else:
            st.warning("No data available")

    elif choice == "View by ID":
        st.subheader("View Data by ID")
        patient_id = st.text_input("Enter Patient ID")
        if st.button("View"):
            data = get_patient_data(patient_id)
            if data:
                df = pd.DataFrame([data], columns=["ID", "Name", "Age", "Medical History", "Created At", "Gender"])
                st.table(df.style.hide(axis=0))
            else:
                st.warning("No record found")

    elif choice == "Update":
        st.subheader("Update Data")
        id = st.text_input("Enter Patient ID to Update")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        medical_history = st.text_area("Medical History")
        gender = st.selectbox("Gender", ["M", "F", "Other"])
        
        if st.button("Update"):
            update_data(id, name, age, medical_history, gender)

    elif choice == "Delete":
        st.subheader("Delete Data")
        id = st.text_input("Enter Patient ID to Delete")
        if st.button("Delete"):
            delete_data(id)

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.success("Logged out successfully")
        st.experimental_rerun()