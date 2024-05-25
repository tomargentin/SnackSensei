import streamlit as st
from PIL import Image, ImageEnhance
import base64
import os

def data(user_info, age_group, food_type, medical_history_path, diet_type, weekly_plan):
    # Process the data as needed
    return {
        "user_info": user_info,
        "age_group": age_group,
        "food_type": food_type,
        "medical_history_path": medical_history_path,
        "diet_type": diet_type,
        "weekly_plan": weekly_plan
    }

# Set up the initial configuration
st.set_page_config(page_title="Nutrition App", layout="centered")

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
        page5
    ]

    pages[st.session_state.page](next_page, prev_page)

# Helper function to add background image
def add_background(page_num):
    image_path = f"images/{page_num}.png"
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
            opacity: 0.5;
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

# Page 5: Type of Diet
def page5(next_page, prev_page):
    add_background(5)
    st.title("Type of Diet")

    if "diet_type" not in st.session_state:
        st.session_state.diet_type = "Diet1"

    st.session_state.diet_type = st.radio("", ["Diet1", "Diet2", "Diet3"])

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Back", key="back_button_page5"):
            prev_page()
    with col2:
        if st.button("Next", key="next_button_page5"):
            # Call the data processing function with all the gathered information
            processed_data = data(
                user_info=st.session_state.user_info,
                age_group=st.session_state.age_group,
                food_type=st.session_state.food_type,
                medical_history_path=st.session_state.medical_history,
                diet_type=st.session_state.diet_type,
                weekly_plan=st.session_state.weekly_plan if "weekly_plan" in st.session_state else None
            )
            st.write("Data processed:", processed_data)
            next_page()

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
