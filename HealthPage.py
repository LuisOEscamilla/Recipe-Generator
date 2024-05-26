import streamlit as st
import os
import base64
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.cloud import texttospeech
from google.cloud import bigquery
from datetime import datetime
from bigquery import get, addto
import time
import main

# Configure Streamlit
st.set_page_config(page_title="Health Recipes By Gemini")
st.header("Welcome " + main.user_name)
# Initialize session state
if 'page_name' not in st.session_state:
    st.session_state.page_name = "health_page.py"
else:
    st.session_state.page_name = "health_page.py"

# Configure generative AI
genai.configure(api_key='AIzaSyAJh77hTTs7oomapWTmVIpUqsokqtBamto')  # API key
model = genai.GenerativeModel('gemini-pro')
vertexai.init(project="raycastanedatechx24", location = "us-central1")    
image_model = ImageGenerationModel.from_pretrained("imagegeneration@005")

#tests to make sure set is empty
def is_empty(ingredients_set):
    if len(ingredients_set) == 0:
        return True
    return False

# Initialize list to store ingredients
if 'health_ingredients' not in st.session_state:
    st.session_state.health_ingredients = set()
    assert is_empty(st.session_state.health_ingredients)


# Streamlit UI components
st.title("Health Recipe Generator💪")

#adds slidebars for protein, carb and calorie counts
protein_min, protein_max = st.slider(
    'Protein range(grams):',value=[0,100])

carb_min, carb_max = st.slider(
    'Carb range(grams):',value=[0,100])

calorie_min, calorie_max = st.slider(
    'Calorie range(kcal):',value=[0,1500])


# Text input for ingredients
ingredient = st.text_input('Enter Ingredient', key='ingredient_input')
if ingredient:
    st.session_state.health_ingredients.add(ingredient)
    st.write('The last added ingredient was:', ingredient)



# Button to display all ingredients
if st.button("Display Ingredients"):
    if st.session_state.health_ingredients:
        st.write("All Ingredients:")
        for i in st.session_state.health_ingredients:
            st.write(i)
    else:
        st.write("No ingredients added yet.")

# Button to reset ingredients list
if st.button("Reset Ingredients"):
    st.session_state.health_ingredients = set()

# Function to generate recipe
def generate_recipe(ingredients):
    addto(ingredients, "health")
    ingredients = ', '.join(ingredients)
    response = model.generate_content("Generate a recipe from the following ingredients: " + ingredients + 
    "Ensure that the recipe meets the following criteria:" + 
    "- Protein content: between " + str(protein_min) + " and " + str(protein_max) + " grams." +
    "- Carbohydrate content: between " + str(carb_min) + " and " + str(carb_max) + " grams." +
    "- Calorie content: between " + str(calorie_min) + " and " + str(calorie_max) + " calories." + 
    "Provide the total calories, protein, and carbs in the recipe, along with tips on how to adjust these values if needed." +
    "If it's not possible to create a recipe meeting the given criteria, return 'Cannot generate a recipe with the given criteria'.")
    
    return response.text

# Function to generate image from recipe
def generate_image(recipe):
    recipe = "Generate what the folllowing would look like: " + recipe 
    images = image_model.generate_images(prompt=recipe)
    if images:
        location = "healthy_recipe_image.jpg"
        images[0].save(location)
        st.image(location)
        return location

    
#tests to make sure something is being generated by the AI
def is_recipe(recipe):
    if len(recipe) != 0:
        return True
    return False

def download_recipe(recipe):
    b64 = base64.b64encode(recipe.encode()).decode()
    new_filename = "healthy_recipe.txt"
    href = f'<a href="data:text/plain;base64,{b64}" download="{new_filename}" style="color: black; text-decoration: none;">Download Recipe</a>'
    styled_link = f'<div style="background-color: white; padding: 5px; border-radius: 5px; display: inline-block;">{href}</div>'
    st.markdown(styled_link, unsafe_allow_html=True)
    st.markdown('<div style="padding-top: 20px;"></div>', unsafe_allow_html=True)
    # st.markdown(href, unsafe_allow_html=True)


def download_image(image_path):
    with open(image_path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode()
    new_filename = "healthy_recipe_image.png"
    href = f'<a href="data:image/png;base64,{b64}" download="{new_filename}" style="color: black; text-decoration: none;">Download Image</a>'
    styled_link = f'<div style="background-color: white; padding: 5px; border-radius: 5px; display: inline-block;">{href}</div>'
    st.markdown(styled_link, unsafe_allow_html=True)
    # st.markdown(href, unsafe_allow_html=True)


# Button to generate recipe and image
if st.button("Generate Recipe"):
    if st.session_state.health_ingredients:
        recipe = generate_recipe(st.session_state.health_ingredients)
        assert is_recipe(recipe)
        st.write(recipe)
        download_recipe(recipe)
        image_path = generate_image(recipe)
        download_image(image_path)
    
        
    else:
        st.write('Please provide the ingredients so I can generate a recipe for you.')

st.subheader("Recently Processed Ingredients")
if st.session_state.page_name == "health_page.py":

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.write(get(5,"health")[i][0])