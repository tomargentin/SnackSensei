import streamlit as st
from PIL import Image, ImageEnhance

# Set up the initial configuration
st.set_page_config(page_title="Nutrition App", layout="centered")

# CSS styles for modern design
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        margin: 0;
        padding: 0;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    .stButton>button {
        background-color: #000000;
        color: #ffffff;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #333333;
    }
    .background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        object-fit: cover;
        opacity: 0.5;
    }
    </style>
    """,
    unsafe_allow_html=True
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
        page6
    ]

    pages[st.session_state.page](next_page, prev_page)

# Helper function to add background image
def add_background(page_num):
    image_path = f"images/{page_num}.png"
    try:
        image = Image.open(image_path)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.5)  # Adjust transparency here
        image.save("images/background_temp.png")
        st.markdown(f"""
            <div class="background">
                <img src="images/background_temp.png" class="background">
            </div>
            """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.write("Image not found. Please ensure the image is named correctly and placed in the images folder.")

# Page 1: User Information
def page1(next_page, prev_page):
    add_background(1)
    st.title("User Information")
    st.text_input("Name")
    st.text_input("Email")
    st.text_input("Phone")
    if st.button("Submit"):
        next_page()

# Page 2: Age Selection
def page2(next_page, prev_page):
    add_background(2)
    st.title("Select Your Age Group")
    age_group = st.radio("", ["18-30", "30-50", "50-60", "60+"])
    if st.button("Next"):
        next_page()
    if st.button("Back"):
        prev_page()

# Page 3: Type of Food
def page3(next_page, prev_page):
    add_background(3)
    st.title("Type of Food")
    food_type = st.selectbox("", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    if st.button("Next"):
        next_page()
    if st.button("Back"):
        prev_page()

# Page 4: Medical History
def page4(next_page, prev_page):
    add_background(4)
    st.title("Medical History")
    st.file_uploader("Upload PDF", type=["pdf"])
    if st.button("Next"):
        next_page()
    if st.button("Back"):
        prev_page()

# Page 5: Type of Diet
def page5(next_page, prev_page):
    add_background(5)
    st.title("Type of Diet")
    diet_type = st.radio("", ["Diet1", "Diet2", "Diet3"])
    if st.button("Next"):
        next_page()
    if st.button("Back"):
        prev_page()

# Page 6: Weekly Plan
def page6(next_page, prev_page):
    add_background(6)
    st.title("Weekly Plan")
    st.write("Plan your meals for the week:")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meals = ["Breakfast", "Lunch", "Dinner"]
    for day in days:
        st.subheader(day)
        for meal in meals:
            st.text_input(f"{day} {meal}")
    if st.button("Back"):
        prev_page()

if __name__ == "__main__":
    main()
