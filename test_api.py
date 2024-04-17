import requests
import json

class TestRecommendAPI:
    def __init__(self):
        self.api_url = 'http://localhost:5000/recommend'
        self.headers = {'Content-Type': 'application/json'}

    def test_recommend_endpoint_happy_path(self):
        data = {
            'Emotion': 'happy',
            'Age': 25,
            'Location': 'Ottawa, Ontario, Canada'
        }
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        assert response.status_code == 200
        recommendations = response.json()
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

    def test_invalid_emotion(self):
        data = {
            'Emotion': 'excited',  # Invalid emotion
            'Age': 25,
            'Location': 'Timmins, Ontario, Canada'
        }
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        assert response.status_code == 400  # Expecting failure due to invalid "Emotion"

    def test_age_below_minimum(self):
        data = {
            'Emotion': 'happy',
            'Age': 4,  # Below the minimum age
            'Location': 'Stockton, California, USA'
        }
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        assert response.status_code == 400  # Expecting failure due to age being too low

    def test_age_above_maximum(self):
        data = {
            'Emotion': 'happy',
            'Age': 121,  # Above the maximum age
            'Location': 'Ottawa, Ontario, Canada'
        }
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        assert response.status_code == 400  # Expecting failure due to age being too high

    def test_missing_age_parameter(self):
        data = {
            'Emotion': 'happy',
            'Location': 'Ottawa, Ontario, Canada'
        }
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        assert response.status_code == 400  # Expecting failure due to missing "Age"

    def test_missing_location_parameter(self):
        data = {
            'Emotion': 'happy',
            'Age': 25
            # 'Location' is omitted
        }
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))
        assert response.status_code == 400  # Expecting failure due to missing "Location"

# Function to run all tests
def run_tests():
    tester = TestRecommendAPI()
    tester.test_recommend_endpoint_happy_path()
    tester.test_invalid_emotion()
    tester.test_age_below_minimum()
    tester.test_age_above_maximum()
    tester.test_missing_age_parameter()
    tester.test_missing_location_parameter()
    print("All tests executed.")

if __name__ == "__main__":
    run_tests()
