import streamlit as st
import random
import math
import base64

# ---------- Must be the first Streamlit command ---------- #
st.set_page_config(page_title="🎯 Number Guessing Game", layout="centered")

# ---------- Set Background from Local Image ---------- #
def set_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Poppins&display=swap');

        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            font-family: 'Poppins', sans-serif;
            color: #FFD700;
        }}

        h1 {{
            font-family: 'Cinzel', serif;
            font-size: 42px;
            color: #FFD700;
            text-align: center;
            text-shadow: 1px 1px 8px #000;
        }}

        .stButton>button {{
            background-color: #1E90FF;
            color: white;
            border: 2px solid #FFD700;
            border-radius: 10px;
            padding: 10px 24px;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
        }}

        .stButton>button:hover {{
            background-color: #FFD700;
            color: black;
        }}

        .stTextInput>div>input,
        .stNumberInput>div>input {{
            background-color: rgba(0,0,0,0.3);
            color: #FFD700;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------- Apply Background ---------- #
set_bg_from_local("grou.jpg")  # Change filename if needed

# ---------- Title ---------- #
st.markdown("<h1>🎯 Welcome to the Number Guessing Game!</h1>", unsafe_allow_html=True)

# ---------- Initialize Session State ---------- #
if "stage" not in st.session_state:
    st.session_state.stage = "init"
    st.session_state.count = 0
    st.session_state.rand = None
    st.session_state.max_guess = 0

# ---------- Game Setup Stage ---------- #
if st.session_state.stage == "init":
    st.markdown("### Select your number range:")

    col1, col2, col3 = st.columns([3, 1, 3])
    with col1:
        lower = st.number_input("Lower Bound", min_value=0, step=1, key="lower")
    with col2:
        st.markdown("<p style='text-align:center;padding-top:10px;'>to</p>", unsafe_allow_html=True)
    with col3:
        upper = st.number_input("Upper Bound", min_value=lower + 1, step=1, key="upper")

    if st.button("🎮 Start Game"):
        st.session_state.low = lower
        st.session_state.high = upper
        st.session_state.rand = random.randint(lower, upper)
        st.session_state.max_guess = math.ceil(math.log2(upper - lower + 1))
        st.session_state.count = 0
        st.session_state.stage = "playing"
        st.success(f"Game started! You have {st.session_state.max_guess} chances to guess a number between {lower} and {upper}.")

# ---------- Game Playing Stage ---------- #
if st.session_state.stage == "playing":
    guess = st.number_input("Enter your guess:", min_value=st.session_state.low, max_value=st.session_state.high, step=1, key="guess")

    if st.button("🚀 Submit Guess"):
        st.session_state.count += 1
        if guess == st.session_state.rand:
            st.success(f"🎉 Correct! You guessed the number {st.session_state.rand} in {st.session_state.count} attempts.")
            st.session_state.stage = "init"
        elif st.session_state.count >= st.session_state.max_guess:
            st.error(f"😢 Out of tries! The number was {st.session_state.rand}.")
            st.session_state.stage = "init"
        elif guess < st.session_state.rand:
            st.warning("📉 Too low! Try a higher number.")
        else:
            st.warning("📈 Too high! Try a lower number.")
