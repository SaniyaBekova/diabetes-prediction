from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import kagglehub
from kagglehub import KaggleDatasetAdapter

app = Flask(__name__)

# Swagger config
app.config['SWAGGER'] = {
    'title': 'Diabetes Prediction API',
    'uiversion': 3
}
swagger = Swagger(app)

# SQLite DB setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diabetes.db'
db = SQLAlchemy(app)

class Diabetes(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Pregnancies = db.Column(db.Integer)
    Glucose = db.Column(db.Integer)
    BloodPressure = db.Column(db.Integer)
    SkinThickness = db.Column(db.Integer)
    Insulin = db.Column(db.Integer)
    BMI = db.Column(db.Float)
    DiabetesPedigreeFunction = db.Column(db.Float)
    Age = db.Column(db.Integer)
    Outcome = db.Column(db.Integer)

# Create the database
with app.app_context():
    db.create_all()

# Global variables for model and encoder
model = None

@app.route('/reload', methods=['POST'])
def reload_data():
    '''
    Reload diabetes dataset from the kaggle, clear the database, load new data, and return summary stats.
    ---
    responses:
      200:
        description: Summary statistics of reloaded data
    '''
    global model

    # Step 1: Download and decompress data

    # Download latest version

    # Set the path to the file you'd like to load
    file_path = "diabetes.csv"

    # Load the latest version
    diabetes = kagglehub.load_dataset(
      KaggleDatasetAdapter.PANDAS,
      "mathchi/diabetes-data-set",
      file_path
    )

    print("First 5 records:", diabetes.head())

    # Step 3: Clear the database
    db.session.query(Diabetes).delete()

    # Step 4: Process data and insert it into the database
    diabetes = diabetes[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']].dropna()

    for ind, row in diabetes.iterrows():
        new_diabetes = Diabetes(
            Id = ind,
            Pregnancies=int(row['Pregnancies']),
            Glucose=int(row['Glucose']),
            BloodPressure=int(row['BloodPressure']),
            SkinThickness=int(row['SkinThickness']),
            Insulin=int(row['Insulin']),
            BMI=float(row['BMI']),
            DiabetesPedigreeFunction = float(row['DiabetesPedigreeFunction']),
            Age=int(row['Age']),
            Outcome=int(row['Outcome'])
        )
        db.session.add(new_diabetes)
    db.session.commit()

    # Step 5: Preprocess and train model
    X = diabetes.drop(columns=['Outcome'])
    y = diabetes['Outcome']
    
    model = RandomForestClassifier(max_depth=2, random_state=0)
    model.fit(X, y)

    # Step 6: Generate summary statistics
    summary = {
        'total_listings': len(diabetes),
        'average_pregnancies': diabetes['Pregnancies'].mean(),
        'average_glucose': diabetes['Glucose'].mean(),
        'average_blood_pressure': diabetes['BloodPressure'].mean(),
        'average_skin_thickness': diabetes['SkinThickness'].mean(),
        'average_insulin': diabetes['Insulin'].mean(),
        'average_bmi': diabetes['BMI'].mean(),
        'average_diabetes_pedigree_function': diabetes['DiabetesPedigreeFunction'].mean(),
        'average_age': diabetes['Age'].mean(),
        'average_outcome': diabetes['Outcome'].mean()
    }

    return jsonify(summary)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Diabetes prediction.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            Pregnancies:
              type: integer
            Glucose:
              type: integer
            BloodPressure:
              type: integer
            SkinThickness:
              type: integer
            Insulin:
              type: integer
            BMI:
              type: number
            DiabetesPedigreeFunction:
              type: number
            Age:
              type: integer
    responses:
      200:
        description: Predicted rental price
    '''
    global model  # Ensure that the model is available for prediction

    # Check if the model and encoder are initialized
    if model is None:
        return jsonify({"error": "The data has not been loaded. Please refresh the data by calling the '/reload' endpoint first."}), 400

    data = request.json
    try:
        Pregnancies = pd.to_numeric(data.get('Pregnancies'), errors='coerce')
        Glucose = pd.to_numeric(data.get('Glucose'), errors='coerce')
        BloodPressure = pd.to_numeric(data.get('BloodPressure'), errors='coerce')
        SkinThickness = pd.to_numeric(data.get('SkinThickness'), errors='coerce')
        Insulin = pd.to_numeric(data.get('Insulin'), errors='coerce')
        BMI = pd.to_numeric(data.get('BMI'), errors='coerce')
        DiabetesPedigreeFunction = pd.to_numeric(data.get('DiabetesPedigreeFunction'), errors='coerce')
        Age = pd.to_numeric(data.get('Age'), errors='coerce')

        if None in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]:
            return jsonify({"error": "Missing or invalid required parameters"}), 400

        # Check for NaN values in the converted inputs
        if pd.isna(Pregnancies) or pd.isna(Glucose) or pd.isna(BloodPressure) or pd.isna(SkinThickness) or pd.isna(Insulin) or pd.isna(BMI) or pd.isna(DiabetesPedigreeFunction) or pd.isna(Age):
            return jsonify({"error": "Invalid numeric values for one or more parameters"}), 400

        # Transform the input using the global encoder
        input_data = np.array([Pregnancies, Glucose, BloodPressure, 
                       SkinThickness, Insulin, BMI, 
                       DiabetesPedigreeFunction, Age])

        input_data = input_data.reshape(1, -1)


        # Predict the diabetes
        predicted_diabetes = model.predict(input_data)[0]
        print("Predicted diabetes:", predicted_diabetes)

        return jsonify({"diabetes": int(predicted_diabetes)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)