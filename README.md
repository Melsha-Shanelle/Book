# Mood Reads - Emotion-Based Book Recommendation System

A personalized book recommendation system that suggests books based on your current emotional state. The app uses facial expression recognition or manual emotion selection to match you with books that suit your mood.

## Features

- **Facial Expression Detection**: Uses your webcam to detect your current emotion using the FER (Facial Expression Recognition) library
- **Manual Emotion Selection**: Choose your emotion manually (happy, sad, angry, neutral)
- **Personalized Recommendations**: Get book recommendations based on your emotion, age, and location
- **Content-Based Filtering**: Uses cosine similarity to match user profiles with book metadata

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Flask REST API
- **ML/AI**:
  - FER (Facial Expression Recognition) for emotion detection
  - BERT model for book emotion classification (pre-trained)
  - Scikit-learn for recommendation engine
- **Data Processing**: Pandas, NumPy

## Project Structure

```
Book/
├── App.py              # Flask API server
├── home.py             # Streamlit frontend
├── Recommender.py      # Recommendation engine
├── model.py            # BERT model training script (Colab)
├── Custom-Model.pth    # Pre-trained BERT model weights
├── FinalFiltering.csv  # Book dataset with emotions (Git LFS)
├── locations.txt       # Valid location options
├── styles.css          # Frontend styling
├── requirements.txt    # Python dependencies
└── tests/
    ├── test_api.py
    ├── test_home.py
    └── test_recommender.py
```

## Installation

### Prerequisites

- Python 3.8+
- Git LFS (for downloading the dataset)

### Setup

1. **Clone the repository with Git LFS**:
   ```bash
   git lfs install
   git clone https://github.com/Melsha-Shanelle/Book.git
   cd Book
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify the dataset** (FinalFiltering.csv should be ~300MB):
   ```bash
   ls -lh FinalFiltering.csv
   ```
   If the file is only a few bytes, run:
   ```bash
   git lfs pull
   ```

## Running the Application

You need to run **two servers** simultaneously:

### 1. Start the Flask API (Backend)

```bash
python App.py
```
The API will run on `http://localhost:5000`

### 2. Start the Streamlit App (Frontend)

In a new terminal:
```bash
streamlit run home.py
```
The app will open in your browser at `http://localhost:8501`

## Usage

1. Open `http://localhost:8501` in your browser
2. Click **Continue** on the welcome page
3. Choose how to input your emotion:
   - **Use Facial Expression**: Allow camera access and click "Analyze Emotion"
   - **Select an Emotion**: Choose from sad, happy, angry, or neutral
4. Enter your **age** and select your **location**
5. Click **Recommend Books** to get personalized suggestions

## API Endpoints

### POST /recommend

Get book recommendations based on user input.

**Request Body**:
```json
{
  "Age": 25,
  "Emotion": "happy",
  "Location": "new york, new york, usa"
}
```

**Response**:
```json
[
  {
    "Book-Title": "Example Book",
    "Book-Author": "Author Name",
    "Year-Of-Publication": "2020",
    "Image-URL-L": "http://..."
  }
]
```

## How It Works

1. **Emotion Detection**: The FER library analyzes facial expressions to detect emotions (angry, happy, sad, fear, surprise, disgust, neutral)

2. **Book Emotion Labeling**: Books in the dataset were pre-labeled with emotions using a fine-tuned BERT model trained on text emotion classification

3. **Recommendation Algorithm**:
   - User features (age, location, emotion) are encoded using OneHotEncoder and StandardScaler
   - Book features are similarly encoded
   - Cosine similarity is computed between user and book feature vectors
   - Scores are adjusted by book ratings
   - Top 5 books with images are returned

## Model Training (Optional)

The `model.py` file contains the code used to train the BERT model on Google Colab. The pre-trained weights are saved in `Custom-Model.pth`.

To retrain:
1. Upload `model.py` to Google Colab
2. Connect to a GPU runtime
3. Run all cells to train the emotion classifier
4. Download the new model weights

## Troubleshooting

### "No module named 'moviepy.editor'"
Install the compatible moviepy version:
```bash
pip install moviepy==1.0.3
```

### Port 5000 already in use (macOS)
Disable AirPlay Receiver in System Settings, or run Flask on a different port:
```bash
flask run --port 5001
```
(Update the API URL in `home.py` accordingly)

### FinalFiltering.csv shows as a small text file
The file is stored with Git LFS. Pull the actual data:
```bash
git lfs pull
```

## License

This project was developed as a Final Year Project (FYP).

## Acknowledgments

- [FER Library](https://github.com/justinshenk/fer) for facial expression recognition
- [Hugging Face Transformers](https://huggingface.co/transformers/) for BERT implementation
- Book dataset derived from public book rating datasets
