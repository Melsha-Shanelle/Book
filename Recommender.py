import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
import joblib


def load_dataset(filepath):
    return pd.read_csv(filepath, dtype={'Year-Of-Publication': str, 'Emotion': str})


def get_user_preprocessor():
    user_categorical_cols = ['Location', 'Emotion']
    user_numerical_cols = ['Age']
    
    user_preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), user_numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), user_categorical_cols)
        ])
    return user_preprocessor

# Function to get recommendations, prioritizing books with images
def get_recommendations(user_input, df_book_final, user_preprocessor):
    user_input_df = pd.DataFrame([user_input])
    user_input_transformed = user_preprocessor.fit_transform(user_input_df)

    book_features = df_book_final[['Age', 'Location', 'Emotion']]
    book_ratings = df_book_final['Book-Rating'].values.reshape(-1, 1)

    book_features_transformed = user_preprocessor.transform(book_features)

    scaler = MinMaxScaler()
    normalized_ratings = scaler.fit_transform(book_ratings)

    similarity_scores = cosine_similarity(user_input_transformed, book_features_transformed)
    adjusted_scores = similarity_scores.flatten() * normalized_ratings.flatten()

    # Sort books by adjusted_scores and iterate to ensure image availability
    sorted_indices = adjusted_scores.argsort()[::-1]
    recommended_books = []
    for index in sorted_indices:
        if len(recommended_books) >= 5:  
            break
        book = df_book_final.iloc[index]
        if pd.notnull(book['Image-URL-L']):  
            recommended_books.append(book)
    
    # Convert the list of Series objects to a DataFrame
    top_books_df = pd.DataFrame(recommended_books).reset_index(drop=True)
    return top_books_df
