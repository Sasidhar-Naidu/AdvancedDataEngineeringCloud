import json
import pymysql
import os
from datetime import datetime

# Database settings
rds_host = os.environ['DB_HOST']
db_username = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError("Unknown type")

def lambda_handler(event, context):
    # Connect to MySQL database
    connection = pymysql.connect(
        host=rds_host,
        user=db_username,
        passwd=db_password,
        db=db_name
    )
    
    cursor = connection.cursor()
    
    # Create a new patient
    if event['httpMethod'] == 'POST' and event['path'] == '/patients':
        body = json.loads(event['body'])
        name = body['name']
        age = body['age']
        gender = body['gender']
        medical_history = body['medical_history']
        
        sql = "INSERT INTO patients (name, age, gender, medical_history) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, age, gender, medical_history))
        connection.commit()
        
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Patient created successfully'})
        }
    
    # Retrieve all patients
    elif event['httpMethod'] == 'GET' and event['path'] == '/patients':
        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()
        
        patients = []
        for row in rows:
            patient = {
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'medical_history': row[4]
            }
            # Convert datetime to string if present
            if len(row) > 5 and isinstance(row[5], datetime):
                patient['created_at'] = row[5].strftime('%Y-%m-%d %H:%M:%S')
            patients.append(patient)
        
        return {
            'statusCode': 200,
            'body': json.dumps(patients, default=datetime_handler)
        }
    
    # Retrieve a specific patient by ID
    elif event['httpMethod'] == 'GET' and event.get('pathParameters'):
        patient_id = event['pathParameters']['patientId']
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        row = cursor.fetchone()
        
        if row:
            patient = {
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'medical_history': row[4]
            }
            # Convert datetime to string if present
            if len(row) > 5 and isinstance(row[5], datetime):
                patient['created_at'] = row[5].strftime('%Y-%m-%d %H:%M:%S')
            return {
                'statusCode': 200,
                'body': json.dumps(patient, default=datetime_handler)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Patient not found'})
            }
    
    # Update a patient by ID
    elif event['httpMethod'] == 'PUT' and event.get('pathParameters'):
        patient_id = event['pathParameters']['patientId']
        body = json.loads(event['body'])
        name = body['name']
        age = body['age']
        gender = body['gender']
        medical_history = body['medical_history']
        
        sql = "UPDATE patients SET name = %s, age = %s, gender = %s, medical_history = %s WHERE id = %s"
        cursor.execute(sql, (name, age, gender, medical_history, patient_id))
        connection.commit()
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Patient updated successfully'})
        }
    
    # Delete a patient by ID
    elif event['httpMethod'] == 'DELETE' and event.get('pathParameters'):
        patient_id = event['pathParameters']['patientId']
        
        sql = "DELETE FROM patients WHERE id = %s"
        cursor.execute(sql, (patient_id,))
        connection.commit()
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Patient deleted successfully'})
        }
    
    # Close the database connection
    connection.close()
    
    return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Unsupported method'})
    }
