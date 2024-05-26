import streamlit as st
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from st_pages import Page, show_pages
from google.cloud import bigquery
from datetime import datetime
from bigquery import get, addto
import time
import os
import base64
import main

global user_name
user_name = "New User"
# Configure Streamlit
st.set_page_config(page_title="Recipes By Gemini")

# Initialize session state
if 'page_name' not in st.session_state:
    st.session_state.page_name = "main.py"
else:
    st.session_state.page_name = "main.py"

# Configure generative AI
genai.configure(api_key='')  # API key
model = genai.GenerativeModel('gemini-pro')
vertexai.init(project="raycastanedatechx24", location = "us-central1")    
image_model = ImageGenerationModel.from_pretrained("imagegeneration@005")

# Configure BigQuery
client = bigquery.Client()


# Generating sidebar
show_pages(
   [
       Page("./app/log_in.py", "Login"),
       Page("./app/main.py", "Home", "🏠"),
       Page("./app/health_page.py", "Health Chef"),
       Page("./app/drink_page.py", "Drink Chef"),
       Page("./app/quantities.py", "Quant Chef")
   ]
)



# Initialize list to store ingredients
if 'all_ingredients' not in st.session_state:
    st.session_state.all_ingredients = set()

st.header("Welcome " + main.user_name)
# Initialize session state
# Streamlit UI components
st.title("Master Chefs")


# Text input for ingredients
ingredient = st.text_input('Enter Ingredient', key='ingredient_input')
if ingredient:
    st.session_state.all_ingredients.add(ingredient)
    st.write('The last added ingredient was:', ingredient)



# Button to display all ingredients
if st.button("Display Ingredients"):
    if st.session_state.all_ingredients:
        st.write("All Ingredients:")
        for i in st.session_state.all_ingredients:
            st.write(i)
    else:
        st.write("No ingredients added yet.")

# Button to reset ingredients list
if st.button("Reset Ingredients"):
    st.session_state.all_ingredients = set()

# Function to generate recipe
def generate_recipe(ingredients):
    addto(ingredients, 'main')
    ingredients = ', '.join(ingredients)
    response = model.generate_content("Generate recipe from the following ingredients: " + ingredients)
    return response.text

# Function to generate image from recipe
def generate_image(recipe):
    prompt = f"Generate an image of the following drink based on the recipe: {recipe}"
    images = image_model.generate_images(prompt=prompt)
    if images:
        location = "health_image.jpg"
        images[0].save(location)
        st.image(location)
        return location



def download_recipe(recipe):
    b64 = base64.b64encode(recipe.encode()).decode()
    new_filename = "drink_recipe.txt"
    href = f'<a href="data:text/plain;base64,{b64}" download="{new_filename}" style="color: black; text-decoration: none;">Download Recipe</a>'
    styled_link = f'<div style="background-color: white; padding: 5px; border-radius: 5px; display: inline-block;">{href}</div>'
    st.markdown(styled_link, unsafe_allow_html=True)
    st.markdown('<div style="padding-top: 20px;"></div>', unsafe_allow_html=True)
    # st.markdown(href, unsafe_allow_html=True)

def download_image(image_path):
    with open(image_path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode()
    new_filename = "drink_image.png"
    href = f'<a href="data:image/png;base64,{b64}" download="{new_filename}" style="color: black; text-decoration: none;">Download Image</a>'
    styled_link = f'<div style="background-color: white; padding: 5px; border-radius: 5px; display: inline-block;">{href}</div>'
    st.markdown(styled_link, unsafe_allow_html=True)
    # st.markdown(href, unsafe_allow_html=True)



    

# Button to generate recipe and image

if st.button("Generate Recipe"):
    if st.session_state.all_ingredients:
        recipe = generate_recipe(st.session_state.all_ingredients)
        st.write(recipe)
        download_recipe(recipe)
        image_path = generate_image(recipe)
        download_image(image_path)
        
    else:
        st.write('Please provide the ingredients so I can generate a recipe for you.')









st.subheader("Recently Procesed Ingredients")
if st.session_state.page_name == "main.py":

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.write(get(5)[i][0])





#streamlit run main.py --server.enableCORS=false
#streamlit run log_in.py --server.enableCORS = false
