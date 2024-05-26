import streamlit as st
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.cloud import texttospeech
from bigquery import get, addto
import main


# Initialize session state for page
if 'page_name' not in st.session_state:
    st.session_state.page_name = "quantities.py"
else:
    st.session_state.page_name = "quantities.py"

# Configure API key
genai.configure(api_key='')

# Create AI model
model = genai.GenerativeModel('gemini-pro')
st.header("Welcome " + main.user_name)
# Define page title
st.title("Food Macronutrient Calculator")

# User inputs
st.subheader("Enter Food Details")
food_name = st.text_input("Food Name")
num_people = st.number_input("Number of People", min_value=1, value=1, step=1)

# Generate AI response and image
if st.button("Generate"):
    if food_name and num_people:
        # Call the AI model to generate macronutrient values
        addto([food_name],'quant')
        with st.spinner("Generating AI response..."):
            response = model.generate_content(f"Please calculate macronutrients for {food_name} for {num_people} people, include proteins, fat, calories, sugar, and more related to health. Separate the information in a table")
            
            # Display AI response
            st.subheader("AI Response:")
            st.write(response.text)

            # Generate image
        with st.spinner('Generating image...'):
            prompt = f"{food_name}"
            vertexai.init(project="raycastanedatechx24", location="us-central1")
            model = ImageGenerationModel.from_pretrained("imagegeneration@005")
            images = model.generate_images(prompt=prompt)

        if images:
            images[0].save(location="samplefile.jpg")
            st.image("samplefile.jpg", use_column_width=True)

            # Generate audio
        with st.spinner('Generating audio...'):
            client = texttospeech.TextToSpeechClient()
            input_text = texttospeech.SynthesisInput(text=response.text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-AU", ssml_gender=texttospeech.SsmlVoiceGender.MALE)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            response = client.synthesize_speech(request={"input": input_text, "voice": voice, "audio_config": audio_config})
            st.audio(response.audio_content, format='audio/mp3')

#Generates similar recipes
if st.button("Generate Similar Recipes"):
    if food_name:
        # Call the AI model to generate similar recipes
        with st.spinner("Generating AI response..."):
            response = model.generate_content(f"Please suggest recipes similar to {food_name}")
            
            # Display AI response
            st.subheader("AI Response:")
            st.write(response.text)

            # Generate audio
        with st.spinner('Generating audio...'):
            client = texttospeech.TextToSpeechClient()
            input_text = texttospeech.SynthesisInput(text=response.text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            audio_response = client.synthesize_speech(
                request={"input": input_text, "voice": voice, "audio_config": audio_config})

            st.audio(audio_response.audio_content, format='audio/mp3')

#Big query
st.subheader("Recently Procesed Ingredients")
if st.session_state.page_name == "quantities.py":
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.write(get(5,"quant")[i][0])
