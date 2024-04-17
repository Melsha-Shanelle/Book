from flask import Flask, request, jsonify
import Recommender  

app = Flask(__name__)

# Load the final dataset
df_book_final = Recommender.load_dataset('FinalFiltering.csv')

# Get the preprocessor
user_preprocessor = Recommender.get_user_preprocessor()


file_path = 'locations.txt'

# Initialize an empty list to hold the valid locations
valid_locations = []

# Open the file and read the locations
with open(file_path, 'r') as file:
    for line in file:
        # Strip whitespace and add the location to the list if it's not empty
        location = line.strip()
        if location:  # This checks if the location string is not empty
            valid_locations.append(location.lower())  # Ensure locations are in lowercase for comparison

@app.route('/recommend', methods=['POST'])
def recommend():
    # Extract user input from the request
    data = request.json
    print(f"Checking for missing fields in data: {data}")
    missing_fields = [field for field in ['Age', 'Emotion', 'Location'] if field not in data or not data[field]]
    if missing_fields:
        error_message = f'Missing field(s): {", ".join(missing_fields)}'
        print(f"Returning error: {error_message}")
        return jsonify({'error': error_message}), 400

    print("Received data:", data)

    # Validate age
    try:
        age = int(data['Age'])
        if not (5 <= age <= 120):
            return jsonify({'error': 'Age must be between 5 and 120.'}), 400
    except ValueError:
        return jsonify({'error': 'Age must be a valid integer.'}), 400

    # Validate emotion
    valid_emotions = ['angry', 'happy', 'sad', 'neutral']
    emotion = data['Emotion'].lower()  # Ensure the comparison is case-insensitive
    if emotion not in valid_emotions:
        return jsonify({'error': f'Emotion must be one of the following: {", ".join(valid_emotions)}.'}), 400

    # Normalize and validate location
    location_input = data['Location'].lower().strip()
    location_normalized = "n/a, n/a, n/a" if location_input not in valid_locations else location_input
    #print("Valid locations loaded:", valid_locations)

    user_input = {
        'Age': age,
        'Location': location_normalized,
        'Emotion': emotion
    }

    # Get recommendations
    recommendations = Recommender.get_recommendations(user_input, df_book_final, user_preprocessor)
    print("Generated recommendations:", recommendations)

    # Convert recommendations to a format that can be sent as JSON
    recs_to_send = recommendations[['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Image-URL-L']].to_dict(orient='records')
    print("Sending response:", recs_to_send)
    return jsonify(recs_to_send)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

