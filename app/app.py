
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pyodbc
import joblib
import numpy as np
import pandas as pd
from sklearn import preprocessing
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://mp5737:Mina123!@sql-mp.database.windows.net/mydb?driver=ODBC+Driver+18+for+SQL+Server'
db = SQLAlchemy(app)

class PotentialCustomers(db.Model):
    __tablename__ = 'PotentialCustomers'
    __table_args__ = {'schema': 'dbo'}
    # id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False, primary_key=True)
    last_name = db.Column(db.String(45), nullable=False, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(45), nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    smoker = db.Column(db.String(45), nullable=False)
    region = db.Column(db.String(45), nullable=False)
    medical_history = db.Column(db.String(45), nullable=False)
    family_medical_history = db.Column(db.String(45), nullable=False)
    exercise_frequency = db.Column(db.String(45), nullable=False)
    occupation = db.Column(db.String(45), nullable=False)
    coverage_level = db.Column(db.String(45), nullable=False)
    PhoneNumber = db.Column(db.String(45), nullable=True)
    predicted_quotes = db.Column(db.Float, nullable=False)

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
            # print("prediction: ", type(prediction[0].item()))
            # df['predicted_quotes'] = prediction

        
        except Exception as e:
            return jsonify({'error': str(e)})
        

        new_customer = PotentialCustomers(
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            bmi=bmi,
            children=children,
            smoker=smoker,
            region=region,
            medical_history=medical_history,
            family_medical_history=family_medical_history,
            exercise_frequency=exercise_frequency,
            occupation=occupation,
            coverage_level=coverage_level,
            PhoneNumber=PhoneNumber,
            predicted_quotes=prediction[0].item()
        )
        
        # Add the new customer to the database
        db.session.add(new_customer)
        db.session.commit()
        predicted_quote = prediction[0].item()
        message = f"Your health insurance quote is ${predicted_quote:.2f}"
        return jsonify(message)

        # return jsonify(prediction_list)
    else:
        return render_template("index.html")
@app.route("/success")
def success():
    return "Values inserted successfully."

if __name__ == "__main__":
    app.run(debug=True)
