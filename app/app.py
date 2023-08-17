import os
# import pyodbc, struct
# from azure import identity

# from typing import Union
# from fastapi import FastAPI
# from pydantic import BaseModel

# class Person(BaseModel):
#     First_name: str
#     Last_name: Union[str, None] = None
    
# connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

# app = FastAPI()

# @app.get("/")
# def root():
#     print("Root of Person API")
#     try:
#         conn = get_conn()
#         cursor = conn.cursor()

#         # Table should be created ahead of time in production app.
#         cursor.execute("""
#             CREATE TABLE Persons (
#                 ID int NOT NULL PRIMARY KEY IDENTITY,
#                 FirstName varchar(255),
#                 LastName varchar(255)
#             );
#         """)

#         conn.commit()
#     except Exception as e:
#         # Table may already exist
#         print(e)
#     return "Insurance API"

# @app.get("/all")
# def get_persons():
#     rows = []
#     with get_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM Persons")

#         for row in cursor.fetchall():
#             print(row.FirstName, row.LastName)
#             rows.append(f"{row.ID}, {row.FirstName}, {row.LastName}")
#     return rows

# @app.get("/person/{person_id}")
# def get_person(person_id: int):
#     with get_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM Persons WHERE ID = ?", person_id)

#         row = cursor.fetchone()
#         return f"{row.ID}, {row.FirstName}, {row.LastName}"

# @app.post("/Person")
# def create_test(item: Person):
#     with get_conn() as conn:
#         cursor = conn.cursor()
#         cursor.execute(f"INSERT INTO Potential (FirstName, LastName) VALUES (?, ?)", item.First_name, item.Last_name)
#         conn.commit()

#     return item

# def get_conn():
#     credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
#     token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
#     token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
#     SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
#     conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
#     return conn
# import pyodbc

# # Database connection settings
# # server = 'sql-mp.database.windows.net'
# # database = 'mydb'
# # username = 'mp5737'
# # password = 'Khametootfarangi78053'
# # driver = '{ODBC Driver 18 for SQL Server}'
# server = 'sql-mp.database.windows.net'
# database = 'mydb'
# authentication = 'ActiveDirectoryInteractive'
# driver = '{ODBC Driver 18 for SQL Server}'

# # Establishing a database connection with Azure AD authentication
# conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Authentication={authentication}')

# # Establishing a database connection
# # conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# def create_customer(first_name, last_name, minit, street, city, zip_code, dob, gender):
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO [dbo].[Customer] ([First_name], [Last_name], [Street], [City], [ZipCode], [DOB], [Gender])
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (first_name, last_name, street, city, zip_code, dob, gender))
#     conn.commit()
#     cursor.close()

# def read_customers():
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM [dbo].[Customer]')
#     rows = cursor.fetchall()
#     cursor.close()
#     return rows

# def update_customer(old_first_name, old_last_name, new_first_name, new_last_name, new_minit, new_street, new_city, new_zip_code, new_dob, new_gender):
#     cursor = conn.cursor()
#     cursor.execute('''
#         UPDATE [dbo].[Customer]
#         SET [First_name] = ?,
#             [Last_name] = ?,
#             [Minit] = ?,
#             [Street] = ?,
#             [City] = ?,
#             [ZipCode] = ?,
#             [DOB] = ?,
#             [Gender] = ?
#         WHERE [First_name] = ? AND [Last_name] = ?
#     ''', (new_first_name, new_last_name, new_minit, new_street, new_city, new_zip_code, new_dob, new_gender, old_first_name, old_last_name))
#     conn.commit()
#     cursor.close()

# def delete_customer(first_name, last_name):
#     cursor = conn.cursor()
#     cursor.execute('DELETE FROM [dbo].[Customer] WHERE [First_name] = ? AND [Last_name] = ?', (first_name, last_name))
#     conn.commit()
#     cursor.close()

# # Example usage
# create_customer('John', 'Doe', '123 Main St', 'Cityville', 12345, '1990-01-15', 'Male')
# customers = read_customers()
# print(customers)
# # update_customer('John', 'Doe', 'Jonathan', 'Doe', 'J', '456 Elm St', 'Townsville', 54321, '1985-08-20', 'Male')
# # delete_customer('Jonathan', 'Doe')

# # Close the database connection
# conn.close()
# +++++++++++++++++++++++++++++++++++++++
from flask import Flask, render_template, request, redirect, url_for
import pyodbc
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
            return redirect(url_for("success"))
    
    return render_template("index.html")

@app.route("/success")
def success():
    return "Values inserted successfully."

if __name__ == "__main__":
    app.run(debug=True)
