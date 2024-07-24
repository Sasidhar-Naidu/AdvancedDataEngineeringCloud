import streamlit as st
import requests

API_URL = 'https://qmiqg29n3e.execute-api.eu-north-1.amazonaws.com/prod'  # Replace with your actual API Gateway URL

# Streamlit application
st.title('Healthcare Management System')

# Function to create a new patient
def create_patient(name, age, gender, medical_history):
    response = requests.post(f'{API_URL}/userdatacreation', json={'name': name, 'age': age, 'gender': gender, 'medical_history': medical_history})
    return response.json()

# Function to get patients
def get_patients():
    response = requests.get(f'{API_URL}/userdatacreation')
    return response.json()

# Function to get a specific patient by ID
def get_patient(patient_id):
    response = requests.get(f'{API_URL}/userdatacreation/{patient_id}')
    return response.json()

# Function to update a patient
def update_patient(patient_id, name, age, gender, medical_history):
    response = requests.put(f'{API_URL}/userdatacreation/{patient_id}', json={'name': name, 'age': age, 'gender': gender, 'medical_history': medical_history})
    return response.json()

# Function to delete a patient
def delete_patient(patient_id):
    response = requests.delete(f'{API_URL}/userdatacreation/{patient_id}')
    return response.json()

# Sidebar for user input
st.sidebar.title('Patient Operations')
operation = st.sidebar.selectbox('Choose an operation', ['Create Patient', 'Get Patients', 'Get Patient', 'Update Patient', 'Delete Patient'])

if operation == 'Create Patient':
    st.sidebar.subheader('Create Patient')
    name = st.sidebar.text_input('Name')
    age = st.sidebar.number_input('Age', min_value=0)
    gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
    medical_history = st.sidebar.text_area('Medical History')
    if st.sidebar.button('Create'):
        result = create_patient(name, age, gender, medical_history)
        st.write(result)

elif operation == 'Get Patients':
    st.sidebar.subheader('Get Patients')
    if st.sidebar.button('Get'):
        patients = get_patients()
        st.write(patients)

elif operation == 'Get Patient':
    st.sidebar.subheader('Get Patient')
    patient_id = st.sidebar.text_input('Patient ID')
    if st.sidebar.button('Get'):
        patient = get_patient(patient_id)
        st.write(patient)

elif operation == 'Update Patient':
    st.sidebar.subheader('Update Patient')
    patient_id = st.sidebar.text_input('Patient ID')
    name = st.sidebar.text_input('New Name')
    age = st.sidebar.number_input('New Age', min_value=0)
    gender = st.sidebar.selectbox('New Gender', ['Male', 'Female', 'Other'])
    medical_history = st.sidebar.text_area('New Medical History')
    if st.sidebar.button('Update'):
        result = update_patient(patient_id, name, age, gender, medical_history)
        st.write(result)

elif operation == 'Delete Patient':
    st.sidebar.subheader('Delete Patient')
    patient_id = st.sidebar.text_input('Patient ID')
    if st.sidebar.button('Delete'):
        result = delete_patient(patient_id)
        st.write(result)
