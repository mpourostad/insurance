
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pyodbc
import joblib
import numpy as np
import pandas as pd
from sklearn import preprocessing
import json
# from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)
def connect_to_database():
    server = "sql-mp.database.windows.net"
    database = "mydb"
    username = "mp5737"
    password = "Mina123!"
    
    connection_string = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"UID={username};"
        f"PWD={password};"
    )
    
    try:
        connection = pyodbc.connect(connection_string)
        print("Connected to the database.")
        return connection
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
def insert_values(connection, first_name, last_name, age, gender, 
                  bmi, children, smoker, region, medical_history, family_medical_history,
                  exercise_frequency, occupation, coverage_level, PhoneNumber):
    try:
        cursor = connection.cursor()
        query = f"INSERT INTO PotentialCustomers (first_name, last_name, age, gender, bmi, children, smoker, region, medical_history, family_medical_history, exercise_frequency, occupation, coverage_level, PhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, first_name, last_name, age, gender,
        bmi, children, smoker, region, medical_history, family_medical_history, 
        exercise_frequency, occupation, coverage_level, PhoneNumber)
        connection.commit()
        print("Values inserted successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")


# Load label mappings from a JSON file
def load_label_mappings(file_path):
    with open(file_path, 'r') as json_file:
        label_mappings = json.load(json_file)
    return label_mappings

# Map features to their corresponding label using label mappings
def map_features_to_labels(feature_dict, label_mappings):
    mapped_features = {}
    for feature, values in feature_dict.items():
        if feature in label_mappings:
            mapping = label_mappings[feature]
            mapped_values = [mapping[value] if value in mapping else value for value in values]
            mapped_features[feature] = mapped_values
        else:
            mapped_features[feature] = values
    return mapped_features
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        age = request.form["age"]
        gender = request.form["gender"]
        bmi = request.form["bmi"]
        children = request.form["children"]
        smoker = request.form["smoker"]
        region = request.form["region"]
        medical_history = request.form["medical_history"]
        family_medical_history = request.form["family_medical_history"]
        exercise_frequency = request.form["exercise_frequency"]
        occupation = request.form["occupation"]
        coverage_level = request.form["coverage_level"]
        PhoneNumber = request.form["PhoneNumber"]
        
        connection = connect_to_database()
        if connection:
            insert_values(connection, first_name, last_name, age, gender,
        bmi, children, smoker, region, medical_history, family_medical_history, 
        exercise_frequency, occupation, coverage_level, PhoneNumber)
            connection.close()

            # ++++++++++++++++++++++++++++++++++++++++
        loaded_label_mappings = load_label_mappings('../mappings.json') 
        data = {
        'age': [age],
        'gender': [gender],
        'bmi': [bmi],
        'children': [children],
        'smoker': [smoker],
        'region': [region],
        'medical_history': [medical_history],
        'family_medical_history': [family_medical_history],
        'exercise_frequency': [exercise_frequency],
        'occupation': [occupation],
        'coverage_level': [coverage_level],
        }
        
        mapped_data = map_features_to_labels(data, loaded_label_mappings)
        df = pd.DataFrame(mapped_data)
        model_data = joblib.load('../trained_model.pkl')
        try:
            prediction = model_data.predict(df)
            prediction_list = prediction.tolist()
            
            return jsonify(prediction_list)
            
            return jsonify(prediction)
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return render_template("index.html")

# bb

    # ...

            # ++++++++++++++++++++++++++++++++++++++++++
    #         return redirect(url_for("success"))
    
    # return render_template("index.html")

@app.route("/success")
def success():
    return "Values inserted successfully."

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(debug=True)
