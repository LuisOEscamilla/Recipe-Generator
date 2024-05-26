import streamlit as st
import os
import base64
import google.generativeai as genai
import vertexai
import pytest
from vertexai.preview.vision_models import ImageGenerationModel
from bigquery import get, addto
import main

# Configure Streamlit
st.set_page_config(page_title="Drink Recipes By Gemini")


# Configure generative AI
genai.configure(api_key='')  # API key
model = genai.GenerativeModel('gemini-pro')
vertexai.init(project="raycastanedatechx24", location="us-central1")    
image_model = ImageGenerationModel.from_pretrained("imagegeneration@005")
st.header("Welcome " + main.user_name)
# Initialize the list if not already done
if 'drink_ingredients' not in st.session_state:
    st.session_state.drink_ingredients = set()

def main():
    # Initialize page session state
    if 'page_name' not in st.session_state:
        st.session_state.page_name = "drink_page.py"
    else:
        st.session_state.page_name = "drink_page.py"

    # Streamlit UI components
    st.title("Drink Recipe Generator🍹")

if __name__ == "__main__":
    main()

# Input for ingredients
ingredient = st.text_input('Enter a drink ingredient (e.g., Banana, Orange)', key='ingredient_input')
if ingredient:
    st.session_state.drink_ingredients.add(ingredient)
    all_ingredients = ", ".join(st.session_state.drink_ingredients)
    st.write('The most recently ingredients added:', all_ingredients)

# Add a dropdown menu for the type of drink to be generated
drink_type = st.selectbox(
    "Select the type of drink you want to generate:",
    ("Cocktail", "Mocktail", "Smoothie", "Other"),
)

# Button to display all ingredients
if st.button("Display Ingredients"):
    if st.session_state.drink_ingredients:
        st.write("All Ingredients:")
        for i in st.session_state.drink_ingredients:
            st.write(i)
    else:
        st.write("No ingredients added yet.")
        

# Button to reset ingredients list
if st.button("Reset Ingredients"):
    st.session_state.drink_ingredients = set()


# Function to generate drink recipe
def generate_recipe(ingredients, drink_type):
    addto(ingredients, "drink")
    # Joining the list of ingredients into a string
    ingredients = ', '.join(ingredients)
    prompt = f"Generate a {drink_type} recipe from the following ingredients: {ingredients}"
    response = model.generate_content(prompt)
    return response.text


# Function to generate image from recipe
def generate_image(recipe):
    prompt = f"Generate an image of the following drink based on the recipe: {recipe}"
    images = image_model.generate_images(prompt=prompt)
    if images:
        location = "drink_image.jpg"
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
if st.button("Generate Drink Recipe"):
    if st.session_state.drink_ingredients:
        recipe = generate_recipe(st.session_state.drink_ingredients, drink_type)
        st.write(f"Here's a crafted {drink_type} just for you:")
        st.write(recipe)
        download_recipe(recipe)
        image_path = generate_image(recipe)
        download_image(image_path)
    else:
        st.write('Please add some ingredients to conjure up a magical drink recipe.')


def main():
    # Display recently processed ingredients
    st.subheader("Recently Procesed Ingredients")
    if st.session_state.page_name == "drink_page.py":
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.write(get(5,"drink")[i][0])

if __name__ == "__main__":
    main()


# streamlit run drink_page.py --server.enableCORS=false
