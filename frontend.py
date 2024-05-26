import streamlit as st
from PIL import Image, ImageEnhance
import base64
import os
import json
from prompts import (get_user_first_prompt,
                     get_model_four_diets_answer_robust,
                     get_user_final_prompt,
                     get_detailed_nutrition_plan_robust)
import random
from grocery_finder import GroceryStoreFetcher
from groq import Groq
import requests

def data(user_info, age_group, food_type, medical_history_path, diet_type, weekly_plan, body_focus, allergies, workout_frequency):
    # Process the data as needed
    return {
        "user_info": user_info,
        "age_group": age_group,
        "food_type": food_type,
        "medical_history_path": medical_history_path,
        "diet_type": diet_type,
        "weekly_plan": weekly_plan,
        "body_focus": body_focus,
        "allergies": allergies,
        "workout_frequency": workout_frequency
    }

# Set up the initial configuration
st.set_page_config(page_title="Nutrition App", layout="centered")


client = Groq(
    api_key="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",
)


# Function to navigate between pages
def main():
    if "page" not in st.session_state:
        st.session_state.page = 0

    def next_page():
        st.session_state.page += 1

    def prev_page():
        st.session_state.page -= 1

    pages = [
        page1,
        page2,
        page3,
        page4,
        page5,
        page6,
        page7,
        page8,
        page9,
        page10,
        page11
    ]

    pages[st.session_state.page](next_page, prev_page)

# Helper function to add background image
def add_background(page_num):
    image_path = f"images/background-logo.png"
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        encoded_image = base64.b64encode(image_bytes).decode()

        background_style = f"""
        <style>
        .stApp {{
            background: url(data:image/png;base64,{encoded_image});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            opacity: 1;
        }}
        </style>
        """
        st.markdown(background_style, unsafe_allow_html=True)
    except FileNotFoundError:
        st.write("Image not found. Please ensure the image is named correctly and placed in the images folder.")

# Page 1: User Information
def page1(next_page, prev_page):
    add_background(1)
    st.title("User Information")

    if "user_info" not in st.session_state:
        st.session_state.user_info = {"Name": "", "Email": "", "Phone": ""}

    st.session_state.user_info["Name"] = st.text_input("Name", st.session_state.user_info["Name"])
    st.session_state.user_info["Email"] = st.text_input("Email", st.session_state.user_info["Email"])
    st.session_state.user_info["Phone"] = st.text_input("Phone", st.session_state.user_info["Phone"])
    st.session_state.user_info["Nationality"] = st.text_input("Nationality", st.session_state.user_info.get("Nationality", ""))

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Submit"):
            next_page()

def page2(next_page, prev_page):
    add_background(2)

    st.markdown("""
        <style>
        .stRadio > div { 
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .stRadio div div {
            margin-bottom: 10px;
        }
        .stRadio div div label {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 50px;
            border: 1px solid black;
            border-radius: 50px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stRadio div div label:hover {
            background-color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Select Your Age Group")

    if "age_group" not in st.session_state:
        st.session_state.age_group = "18-25"

    st.session_state.age_group = st.radio("", ["18-25", "26-35", "36-45", "46-55", "56-60", "60+"], index=0)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page2"):
            prev_page()
    with col2:
        if st.button("Next", key="next_button_page2"):
            next_page()

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# Page 3: Type of Food
def page3(next_page, prev_page):
    add_background(3)
    st.title("Type of Food")

    if "food_type" not in st.session_state:
        st.session_state.food_type = "Vegetarian"

    st.session_state.food_type = st.selectbox("Select your food preference", ["Vegetarian", "Non-Vegetarian", "Vegan"],
                                              index=0)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page3"):
            prev_page()
    with col2:
        if st.button("Next", key="next_button_page3"):
            next_page()

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# Page 4: Medical History
def page4(next_page, prev_page):
    add_background(4)
    st.title("Medical History")

    if "medical_history" not in st.session_state:
        st.session_state.medical_history = None

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        file_path = os.path.join("uploaded_files", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.medical_history = file_path
        st.success(f"File saved to {file_path}")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page4"):
            prev_page()
    with col2:
        if st.button("Next", key="next_button_page4"):
            next_page()

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# Page 5: Body Part Focus
def page5(next_page, prev_page):
    add_background(5)
    st.title("Which body part would you like to focus more?")

    if "body_focus" not in st.session_state:
        st.session_state.body_focus = ""

    st.session_state.body_focus = st.text_input("Body Part", st.session_state.body_focus)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page5"):
            prev_page()
    with col2:
        if st.button("Next", key="next_button_page5"):
            next_page()

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# Page 6: Allergies
def page6(next_page, prev_page):
    add_background(6)
    st.title("Are you allergic to something?")

    if "allergies" not in st.session_state:
        st.session_state.allergies = ""

    st.session_state.allergies = st.text_input("Allergies", st.session_state.allergies)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page6"):
            prev_page()
    with col2:
        if st.button("Next", key="next_button_page6"):
            next_page()

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# Page 7: Workout Frequency
def page7(next_page, prev_page):
    add_background(7)
    st.title("How many times do you workout in a week?")

    if "workout_frequency" not in st.session_state:
        st.session_state.workout_frequency = 0

    st.session_state.workout_frequency = st.number_input("Workout Frequency", min_value=0, value=st.session_state.workout_frequency)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page7"):
            prev_page()
    with col2:
        if st.button("Next", key="next_button_page7"):
            # Gather all data and run the prompt
            nationality = st.session_state.user_info["Nationality"]
            body_part = st.session_state.body_focus
            preferred_diet = st.session_state.food_type
            address = st.session_state.user_info.get("Address", "")
            workout_plan = st.session_state.workout_frequency
            age = st.session_state.age_group
            allergies = st.session_state.allergies.split(",") if st.session_state.allergies else []
            medical_report_path = st.session_state.medical_history

            st.session_state.results = get_user_first_prompt(
                nationality=nationality,
                body_part=body_part,
                preferred_diet=preferred_diet,
                address=address,
                workout_plan=workout_plan,
                age=age,
                allergies=allergies,
                medical_report=medical_report_path
            )
            # print(st.session_state.results)
            st.session_state.diets = json.loads(get_model_four_diets_answer_robust(user_prompt=st.session_state.results))["diet_plans"]
            next_page()
    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# Page 8: Display Results
def page8(next_page, prev_page):
    add_background(8)
    st.title(f"Diet Plans just for you {st.session_state.user_info.get('Name')}")

    if "diets" in st.session_state:
        diet_plans = st.session_state.diets

        # Display diet plans
        for i, diet in enumerate(diet_plans):
            st.markdown(
                f"""
                <div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;">
                    <h3>{diet['diet_name']}</h3>
                    <p>{diet['explanation']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("I want this diet!", key=f"diet{i}"):
                st.session_state.activated_card = diet
                next_page()
                return

        st.write("---")  # Separator line

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page8"):
            prev_page()
    st.markdown("""
            <style>
            .stButton button {
                border-radius: 50px;
                width: 100%;
            }
            </style>
        """, unsafe_allow_html=True)



def page9(next_page, prev_page):
    add_background(9)
    if "activated_card" not in st.session_state:
        st.error("No diet plan selected. Please go back and select a diet plan.")
        if st.button("Back"):
            prev_page()
        return

    # Show selected diet plan
    diet_title = st.session_state["activated_card"]["diet_name"]
    diet_explanation = st.session_state["activated_card"]["explanation"]
    st.title(diet_title)  # Display the selected diet title at the top

    user_prompt = f"Based on your selection of {diet_title}, here is the explanation:"
    final_user_prompt = get_user_final_prompt(
        user_prompt, diet_title, diet_explanation
    )
    detailed_nutrition_plan = get_detailed_nutrition_plan_robust(
        final_user_prompt, client
    )
    json_file = json.loads(detailed_nutrition_plan)

    st.write("Diet information:")
    st.title("Weekly Plan")
    st.write("Plan your meals for the week:")

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    meals = ["breakfast", "lunch", "dinner"]

    meal_plan = json_file.get("week_plan", {})

    st.markdown("""
        <style>
            .day-block {
                border: 2px solid #000;
                border-radius: 40px;
                padding: 10px;
                margin-bottom: 20px;
            }
            .meal-block {
                background-color: #FFDAB9;
                border-radius: 20px;
                padding: 10px;
                margin-bottom: 10px;
                color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)

    for day in days:
        st.markdown(f'<div class="day-block"><h2>{day}</h2>', unsafe_allow_html=True)
        if day in meal_plan:
            for meal in meals:
                meal_info = meal_plan[day].get(meal, {})
                meal_name = meal_info.get("name", "Not Provided")
                meal_ingredients = meal_info.get("ingredients", "Not Provided")
                if meal_ingredients != "Not Provided":
                    meal_ingredients = ', '.join(meal_ingredients)
                meal_instructions = meal_info.get("instructions", "Not Provided")

                st.markdown(
                    f"""
                    <div class="meal-block">
                        <h3>{meal.capitalize()} Name</h3>
                        <p>{meal_name}</p>
                        <h3>{meal.capitalize()} Ingredients</h3>
                        <p>{meal_ingredients}</p>
                        <h3>{meal.capitalize()} Recipe</h3>
                        <p>{meal_instructions}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                f"""
                <div class="meal-block">
                    <h3>{meal.capitalize()} Name</h3>
                    <p>Not Provided</p>
                    <h3>{meal.capitalize()} Ingredients</h3>
                    <p>Not Provided</p>
                    <h3>{meal.capitalize()} Recipe</h3>
                    <p>Not Provided</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state["total_quantities"] = json_file.get("total_quantities (grams)", {})

    col1, col2 = st.columns([1, 1])

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Buy groceries"):
            next_page()


import streamlit as st



def fetch_near_grocery_stores_by_address(address, radius=1000.0):
    # TODO: we'll return this
    fetcher = GroceryStoreFetcher(config_file='config.ini')
    coordinates = fetcher.get_coordinates(address)
    all_grocery_stores = []
    if coordinates:
        latitude, longitude = coordinates
        all_grocery_stores = fetcher.fetch_all_grocery_stores(latitude, longitude, radius=radius)
    return all_grocery_stores
    # return ["Grocery Store 1", "Grocery Store 2", "Grocery Store 3", "Grocery Store 4"]

def page10(next_page, prev_page):
    add_background(10)
    st.title("Find Grocery Stores Near You")

    address = st.text_input("Enter your address")
    print("USER ADDRESS --> ", address)
    radius = st.slider("Select distance from your home (meters)", min_value=100, max_value=5000, step=100, value=1000)

    if st.button("Find Stores"):
        stores = fetch_near_grocery_stores_by_address(address=address, radius=radius)
        st.session_state.grocery_stores = stores

    if "grocery_stores" in st.session_state:
        st.multiselect("Select up to 2 grocery stores", st.session_state.grocery_stores, key="selected_stores",
                       max_selections=2)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page10"):
            prev_page()
    with col2:
        if st.button("Next", key="next_button_page10") and "selected_stores" in st.session_state:
            next_page()

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)


# def page11(next_page, prev_page):
#     st.title("Grocery Store Details")
#     print(st.session_state["total_quantities"])
#     ingredients = st.session_state["total_quantities"].keys()
#
#
#     length = len(ingredients)
#
#
#     if "selected_stores" in st.session_state:
#         # TODO: You have to see how many stores user has selected and then select those number of stores from this list only ['aldi', 'kaufland', 'abc', 'pqr']
#         # and send the output to this in the format     "store_name": [
#                                                                 #         "aldi",
#                                                                 #         "abc",
#                                                                 #         "pqr"
#                                                                 #     ] and put this intot he payload below
#
#         # and we already have the keys from the ingrediets pass that here as #{
#         #                                             #     "potatoes": 2000,
#         #                                             #     "carrot": 1000,
#         #                                             #     "chicken": 100,
#         #                                             #     "turnip": 300,
#         #                                             #     "onion": 500
#         #                                             # }
#
#
#
#
#         payload = {
#             "store_name": st.session_state.selected_stores,
#             "ingredients": ingredients
#         }
#
#         # Call the API and get the response
#         response = requests.post("http://127.0.0.1:5000/get-items", json=payload)
#         if response.status_code == 200:
#             store_data = response.json()
#             # Todo: you will get respinse from the API like this - {
#             #     "carrot": {
#             #         "item_name": "Carrot",
#             #         "price": 0.5,
#             #         "store": "abc"
#             #     },
#             #     "chicken": {
#             #         "item_name": "NA",
#             #         "price": "NA",
#             #         "store": "NA"
#             #     },
#             #     "onion": {
#             #         "item_name": "NA",
#             #         "price": "NA",
#             #         "store": "NA"
#             #     },
#             #     "potatoes": {
#             #         "item_name": "Potatoes",
#             #         "price": 0.5,
#             #         "store": "aldi"
#             #     },
#             #     "turnip": {
#             #         "item_name": "Turnip",
#             #         "price": 0.6,
#             #         "store": "pqr"
#             #     }
#             # }
#
#             # you have to get the price for the items selcted and if the price is NA then just neglect that and if the prices is there in float value then multiply it with the quantity we have suggested for example in the ingredients we also have the values for each item,  then just check the keys of the respinse and get the price and multiple and do the total and print the total price
#             #
#
#
#             for item, details in store_data.items():
#                 st.markdown(
#                     f"""
#                     <div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;">
#                         <h3>{details['item_name']}</h3>
#                         <p>Price: {details['price']}</p>
#                         <p>Store: {details['store']}</p>
#                     </div>
#                     """,
#                     unsafe_allow_html=True,
#                 )
#
#     col1, col2 = st.columns([1, 1])
#
#     with col1:
#         if st.button("Back", key="back_button_page11"):
#             prev_page()
#     with col2:
#         if st.button("Next", key="next_button_page11"):
#             next_page()
#
#     st.markdown("""
#         <style>
#         .stButton button {
#             border-radius: 50px;
#             width: 100%;
#         }
#         </style>
#     """, unsafe_allow_html=True)
#
#     import streamlit as st
#     import requests

def page11(next_page, prev_page):
    add_background(10)
    st.title("Grocery Store Details")
    print(st.session_state["total_quantities"])
    ingredients = st.session_state["total_quantities"]

    if "selected_stores" in st.session_state:
        # Get selected stores
        selected_stores = st.session_state.selected_stores

        available_stores = ['aldi', 'kaufland', 'abc', 'pqr']
        num_selected_stores = len(selected_stores)

        # Randomly select the required number of stores from available stores
        stores_to_query = random.sample(available_stores, num_selected_stores)

        payload = {
            "store_name": stores_to_query,
            "ingredients": ingredients
        }

        # Call the API and get the response
        response = requests.post("http://127.0.0.1:5000/get-items", json=payload)
        if response.status_code == 200:
            store_data = response.json()

            total_price = 0

            for item, details in store_data.items():
                if details['price'] != "NA":
                    print("DETAILS", item, details)
                    item_price = float(details['price']) * float(ingredients[item]) / 100
                    total_price += item_price

                    # Randomly select a store from the user's selected stores
                    random_store = random.choice(selected_stores)

                    st.markdown(
                        f"""
                        <div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;">
                            <h3>{details['item_name']}</h3>
                            <p>Price per unit: {details['price']}</p>
                            <p>Store: {random_store}</p>
                            <p>Quantity: {ingredients[item]}</p>
                            <p>Total Price: {item_price}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown(
                f"""
                <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;">
                    <h2>Total Price: {total_price}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page11"):
            prev_page()

    st.markdown("""
        <style>
        .stButton button {
            border-radius: 50px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    # Create the directory to save uploaded files if it doesn't exist
    if not os.path.exists("uploaded_files"):
        os.makedirs("uploaded_files")

    main()


