import pytest
from app import app, db

# Define valid input for prediction test
valid_input = {
  "Age": 49,
  "BMI": 33.6,
  "BloodPressure": 72,
  "DiabetesPedigreeFunction": 0.627,
  "Glucose": 148,
  "Insulin": 0,
  "Pregnancies": 6,
  "SkinThickness": 35
}


# Define missing field input for prediction test
missing_field_input = {
    "Age": 49,
    "BMI": 33.6,
    "BloodPressure": 72,
    "DiabetesPedigreeFunction": 0.627,
    "Glucose": 148,
    "Insulin": 0
}


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_reload_data(client):
    """Test the reload endpoint that loads the data."""
    response = client.post('/reload')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'total_listings' in json_data
    assert 'average_age' in json_data

def test_predict_after_reload(client):
    """Test prediction endpoint after reloading the data."""
    # Reload the data first
    client.post('/reload')

    # Test valid prediction
    response = client.post('/predict', json=valid_input)
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'diabetes' in json_data



def test_missing_fields(client):
    """Test prediction with missing fields."""
    # Reload the data first
    client.post('/reload')

    # Test with missing fields
    response = client.post('/predict', json=missing_field_input)
    assert response.status_code == 400
    json_data = response.get_json()
    assert "Invalid numeric values for one or more parameters" in json_data['error']

