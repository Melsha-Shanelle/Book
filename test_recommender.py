import pytest
import pandas as pd
from Recommender import get_user_preprocessor, get_recommendations, load_dataset

# Mock dataset for testing
mock_data = {
    'Age': [25, 30, 35],
    'Location': ['ottawa, ontario, canada', 'timmins, ontario, canada', 'stockton, california, usa'],
    'Emotion': ['happy', 'sad', 'angry'],
    'Book-Title': ['Book1', 'Book2', 'Book3'],
    'Book-Author': ['Author1', 'Author2', 'Author3'],
    'Year-Of-Publication': ['2001', '2002', '2003'],
    'Image-URL-L': ['url1', 'url2', 'url3'],
    'Book-Rating': [5, 4, 3]
}
df_book_final = pd.DataFrame(mock_data)

def test_preprocessing_pipeline():
    sample_user_input = {'Age': 30, 'Location': 'Ottawa, Ontario, Canada', 'Emotion': 'happy'}
    preprocessor = get_user_preprocessor()
    transformed_input = preprocessor.fit_transform(pd.DataFrame([sample_user_input]))
    assert transformed_input is not None
    assert transformed_input.shape == (1, 3)  

def test_recommendations_output():
    user_input = {'Age': 25, 'Location': 'Ottawa, Ontario, Canada', 'Emotion': 'happy'}
    user_preprocessor = get_user_preprocessor()
    recommendations = get_recommendations(user_input, df_book_final, user_preprocessor)
    assert isinstance(recommendations, pd.DataFrame)
    assert not recommendations.empty
    assert all(col in recommendations.columns for col in ['Book-Title', 'Book-Author', 'Year-Of-Publication', 'Image-URL-L'])


