import streamlit as st
from fer import FER
import numpy as np
from PIL import Image
from streamlit_option_menu import option_menu
import requests

st.set_page_config(page_title="Mood Reads", page_icon=":book:", layout='wide')
# Function to load and inject the CSS file into the Streamlit app
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply the external CSS styles
local_css("styles.css")

st.markdown("""
    <div class="title">
        <h1>
            <img src="https://raw.githubusercontent.com/Melsha-Shanelle/Mood-Reads/3175f10b970b703f63ebb9d929f0894019eea740/specs.png" alt="Mood Reads Logo">
            MOOD READS
        </h1>
    </div>
""", unsafe_allow_html=True)

def filter_books(emotion, age, location):
    api_url = 'http://localhost:5000/recommend'
    data = {'Emotion': emotion, 'Age': age, 'Location': location}
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        recommendations = response.json()
    else:
        st.error('Failed to retrieve recommendations')
        recommendations = []
    return recommendations


# Initialize session state variables
if 'emotion' not in st.session_state:
    st.session_state['emotion'] = None
if 'age' not in st.session_state:
    st.session_state['age'] = 5
if 'location' not in st.session_state:
    st.session_state['location'] = "n/a, n/a, n/a"
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

def show_home_page():
   st.markdown('<div class="big-font">Welcome to Mood Reads!</div>', unsafe_allow_html=True)
   st.markdown('<div class="medium-font">Discover books that match your mood.</div>', unsafe_allow_html=True)
    
   if st.button("Continue"):
        st.session_state['page'] = 'input_emotion'
        st.rerun()

import streamlit as st
from fer import FER
import numpy as np
from PIL import Image

def show_emotion_input_page():

    
    st.markdown('<div class="medium-font">How would you like to input your emotion?</div>', unsafe_allow_html=True)
    
    option = st.radio("", ('Use Facial Expression', 'Select an Emotion'))

    if option == 'Use Facial Expression':
        captured_image = st.camera_input("Take a picture")

        if captured_image is not None:
            detector = FER(mtcnn=True)
            pil_image = Image.open(captured_image)
            image_array = np.array(pil_image)
            st.image(image_array, use_column_width=True)

            if st.button('Analyze Emotion'):
                result = detector.detect_emotions(image_array)

                if result:
                    dominant_emotion, emotion_score = max(result[0]['emotions'].items(), key=lambda item: item[1])
                    filtered_emotions = ["angry", "happy", "sad"]
                    if dominant_emotion in filtered_emotions:
                        st.session_state['emotion'] = dominant_emotion
                    else:
                        st.session_state['emotion'] = "neutral"   
                    st.session_state['page'] = 'input_details' 
                    st.rerun()

    elif option == 'Select an Emotion':
        col, buffer_right = st.columns([2, 8])
        with col:
        
            emotion = st.selectbox("", ['sad', 'happy', 'angry', 'neutral'])
            if st.button('Submit Selected Emotion'):
               st.session_state['emotion'] = emotion
               st.session_state['page'] = 'input_details'
               st.rerun()

            if st.button('Go Back'):
               st.session_state['page'] = 'home'
               st.rerun()


# Function to display details input page
def show_details_input_page():
    st.markdown('<div class="big-font">Enter Your Details</div>', unsafe_allow_html=True)
    col, buffer_right = st.columns([2, 8])
    with col:
        # Age input
        age = st.number_input("Enter Age", min_value=5, max_value=120, step=1, value=st.session_state.get('age', 5))
        
       
        file_path = 'locations.txt'

        # Initialize an empty list to hold the valid locations
        valid_locations = []

        # Open the file and read the locations
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace and add the location to the list if it's not empty
                location = line.strip()
                if location:  # This checks if the location string is not empty
                    valid_locations.append(location)
        
        
        default_index = valid_locations.index("Other / Not Available")
        
        # Location selection
        location = st.selectbox("Select Location", options=valid_locations, index=default_index)
        
        # Convert "Other / Not Available" to "n/a, n/a, n/a" or use the location as is
        location_to_send = "n/a, n/a, n/a" if location == "Other / Not Available" else location.lower()
        
        # Button to proceed and filter books based on the selections
        if st.button('Recommend Books'):
            # Update session state with the selected details
            st.session_state['age'] = age
            st.session_state['location'] = location_to_send
            
            
            st.session_state['filtered_books'] = filter_books(st.session_state['emotion'], age, location_to_send)
            # Navigate to the recommendations page
            st.session_state['page'] = 'show_recommendations'
            st.experimental_rerun()

    if st.button('Go Back to Emotion Input'):
        st.session_state['page'] = 'input_emotion'
        st.experimental_rerun()


def show_recommendations_page():
    st.markdown('<div class="big-font">Book Recommendations</div>', unsafe_allow_html=True)
    
    if 'filtered_books' in st.session_state and st.session_state['filtered_books']:
        for book in st.session_state['filtered_books']:
            col1, col2 = st.columns([1, 3])  
            
           
            if book.get('Image-URL-L'):
                with col1:
                    st.image(book['Image-URL-L'], caption=book['Book-Title'])
            
            
            with col2:
                st.markdown(f"""
               <div style='margin-bottom: 20px;'>
               <p class='big-font'>{book['Book-Title']}</p>
               <p class='medium-font'><b>Author:</b> {book['Book-Author']}</p>
               <p class='medium-font'><b>Year of Publication:</b> {book['Year-Of-Publication']}</p>
               </div>
               """, unsafe_allow_html=True)
            
            # Add a horizontal line for separation between book entries
            st.markdown("---")
    else:
        st.write("No recommendations available. Please adjust your selections and try again.")
    
    if st.button('Go Back'):
        st.session_state['page'] = 'input_details'
        st.rerun()




# Page routing
if st.session_state['page'] == 'home':
    show_home_page()
elif st.session_state['page'] == 'input_emotion':
    show_emotion_input_page()
elif st.session_state['page'] == 'input_details':
    show_details_input_page()
elif st.session_state['page'] == 'show_recommendations':
    show_recommendations_page()


