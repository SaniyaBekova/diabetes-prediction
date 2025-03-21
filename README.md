
# Diabetes Prediction API

This is a Flask-based API that predicts Diabetes based on several factors like Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age. The API has two main endpoints:
- `/reload`: Reloads the data and trains the model.
- `/predict`: Predicts the diabetes for a given parameters.

## Data Source and Prediction Process

### Data Source

The data used for this project comes from the [Kaggle](https://www.kaggle.com/datasets/mathchi/diabetes-data-set/data).

The dataset includes important features such as:
**Pregnancies:** Number of times pregnant
**Glucose:** Plasma glucose concentration a 2 hours in an oral glucose tolerance test
**BloodPressure:** Diastolic blood pressure (mm Hg)
**SkinThickness:** Triceps skin fold thickness (mm)
**Insulin:** 2-Hour serum insulin (mu U/ml)
**BMI:** Body mass index (weight in kg/(height in m)^2)
**DiabetesPedigreeFunction:** Diabetes pedigree function
**Age:** Age (years)
**Outcome:** Class variable (0 or 1)

The full dataset can be accessed and downloaded from the Kaggle website at [Kaggle](https://www.kaggle.com/datasets/mathchi/diabetes-data-set/data).

### Prediction Process

The application uses a **RandomForestClassifier** to predict the likelihood of diabetes based on several medical and physiological input features, including Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age.

The process of prediction is as follows:
1. **Model Training**: The RandomForestClassifier is trained on a cleaned version of the diabetes dataset. The model learns patterns and relationships between input features and the target outcome (presence or absence of diabetes).
2. **Prediction**: After training, the model can predict the probability of a patient having diabetes based on new input data provided by the user through the API.

This approach allows the application to deliver reliable diabetes predictions in real-time using clinically relevant indicators.


## Prerequisites

Before you can set up and run this app, ensure you have the following software installed:

- **Python 3.9+**
- **pip** (Python package installer)
- **Virtualenv** (Optional but recommended)

## Setting up on macOS and Windows

### 1. Clone the Repository
First, clone this repository to your local machine:
```bash
git clone https://github.com/tjhoranumass/airbnb.git
cd airbnb
```

### 2. Create a Virtual Environment (Optional but Recommended)

You can create a virtual environment to isolate the project dependencies.

For macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install the Dependencies

Install the required Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Flask requires some environment variables to run the app correctly. Create a `.env` file in the project root with the following content:

```bash
FLASK_APP=app.py
FLASK_ENV=development
```

For macOS, you can set the environment variables using the following commands:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

For Windows, you can set the environment variables using the following commands in PowerShell:

```bash
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
```

### 5. Initialize the SQLite Database

To set up the SQLite database for the first time, run:

```bash
flask shell
```

Inside the shell, run:
```python
from app import db
db.create_all()
exit()
```

### 6. Running the Application

Once everything is set up, you can run the application with the following command:

```bash
flask run
```

By default, the app will run on [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 7. Swagger Documentation

You can access the Swagger documentation for the API at:

```
http://127.0.0.1:5000/apidocs/
```

### 8. Testing the Endpoints

#### Reload Data

To reload the data and train the model, use the `/reload` endpoint:

```bash
curl -X POST http://127.0.0.1:5000/reload
```

#### Diabetes Prediction

To predict a diabetes, you can use the `/predict` endpoint. Here's an example request:

```bash
curl -X POST "http://127.0.0.1:5000/predict" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"Age\": 49, \"BMI\": 33.6, \"BloodPressure\": 72, \"DiabetesPedigreeFunction\": 0.627, \"Glucose\": 148, \"Insulin\": 0, \"Pregnancies\": 6, \"SkinThickness\": 35}"
```

### 9. Stopping the Application

To stop the Flask app, you can press `Ctrl + C` in the terminal window where the app is running.

---

## Troubleshooting

### Common Issues

- **Environment variables not being set**: Ensure you have set the environment variables correctly, especially when switching between macOS and Windows.

- **Database initialization issues**: If the app crashes because of database-related errors, make sure you have run the `flask shell` commands to initialize the database properly.

- **Dependency issues**: Ensure that you are using the correct version of Python (3.9+) and have installed the dependencies using `pip install -r requirements.txt`.

---

## License

This project is licensed under the MIT License.

## Running Tests

We use `pytest` for running tests on this application. Before running the tests, ensure all dependencies are installed and the application is properly set up.

### Setting up for Testing

1. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

2. Export the `PYTHONPATH` environment variable to ensure Python can locate the app module.

For macOS/Linux:
```bash
export PYTHONPATH=.
```

For Windows (PowerShell):
```bash
$env:PYTHONPATH="."
pytest
```

3. Run the tests:

```bash
pytest
```

This will execute all the tests located in the `tests/` folder and provide feedback on the application behavior.

Deployed API link:


