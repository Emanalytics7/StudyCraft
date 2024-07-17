import streamlit as st
from content_generation import LearningScheduler, APIError
from pdf_conversion import PDFDocument
import os
from datetime import datetime

def main():
    # set page config
    st.set_page_config(page_title="StudyCraft", page_icon="artifacts/swan.png", layout="wide")

    # custom css for light theme with gradient buttons
    st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #45a049, #4CAF50);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stDownloadButton>button {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background: linear-gradient(45deg, #2980b9, #3498db);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stSelectbox {
        background-color: #f8f9fa;
    }
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #333333;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

    # ======<sidebar>=======
    with st.sidebar:
        st.image("artifacts/books.png", width=120)
        st.markdown("<p class='big-font'>Hey there, I'm Eman!</p>", unsafe_allow_html=True)
        st.write("Welcome to my StudyCraft app. Let's craft an awesome learning plan for you!")
        
        st.subheader("What can StudyCraft do?")
        st.write("🟣 Create personalized learning plans")
        st.write("🟢 Cover a variety of subjects")
        st.write("🔴 Adapt to your schedule")
        st.write("🟡 Match your learning style")
        st.write("🔵 Create a PDF for you!")

    # ========<main content>========
    st.title("☆Your Personalized StudyCrafter☆")

    st.write("Let's create an amazing study plan just for you. Fill in these details, and we'll work some magic! 🪄")

    col1, col2, col3 = st.columns(3)

    with col1:
        goal_options = ["Data Science", "Learn Python", "Data Analyst", "Software Engineer", "Graphic Designer", "Other"]
        goal = st.selectbox("What's your learning goal? 🎯", [""] + goal_options)
        if goal == "Other":
            goal = st.text_input("Cool! What specific skill do you want to learn?", "")

    with col2:
        duration = st.selectbox("How long do you want to study? ⏱️", [""] + [f"{i} month{'s' if i > 1 else ''}" for i in range(1, 13)])

    with col3:
        style_options = ["Interactive", "Theoretical", "Practical", "Other"]
        style = st.selectbox("What's your preferred learning style? 🧠", [""] + style_options)
        if style == "Other":
            style = st.text_input("Interesting! How do you like to learn?", "")

    # making sure all inputs are filled
    all_inputs_filled = goal and duration and style and goal != "I want to learn..." and (style != "Other" or (style == "Other" and style != "I learn best by..."))

    if all_inputs_filled:
        st.markdown("### Here you go! Your learning journey awaits...")
        st.markdown("*Psst! I heard clicking buttons is good for your finger muscles. Just saying...*")

    if st.button("Click me, please!🥹", key="generate_plan", disabled=not all_inputs_filled):
        if not all_inputs_filled:
            st.error("Oops! Looks like you missed something. Can you double-check all the fields for me? 🕵️‍♂️")
        else:
            generate_plan_with_api_keys(goal, duration, style)

    # =====<footer>======
    st.markdown("---")
    st.write("Made with ❤️ by Eman | © 2024 StudyCraft")

def generate_plan_with_api_keys(goal, duration, style):
    exa_key_default = os.environ.get('EXA_API_KEY', '')
    groq_key_default = os.environ.get('GROQ_API_KEY', '')

    content, error = generate_plan(exa_key_default, groq_key_default, goal, duration, style)
    
    if error:
        st.error(f"Oops! We hit a snag: {error}")
        st.warning("No worries! Let's try with your own API keys.")
        
        col1, col2 = st.columns(2)
        with col1:
            exa_key = st.text_input("Your EXA API Key (I promise to keep it safe! 🤐)", type="password")
        with col2:
            groq_key = st.text_input("Your GROQ API Key (It's our little secret! 🔒)", type="password")
        
        if st.button("🔄 Let's Try Again!", key="retry"):
            if not exa_key or not groq_key:
                st.error("Hey there! We need both API keys to work our magic. Can you fill them in? 🎩✨")
            else:
                content, error = generate_plan(exa_key, groq_key, goal, duration, style)
                
                if error:
                    st.error(f"Uh-oh! Another hiccup: {error}")
                else:
                    create_pdf(content)
    else:
        create_pdf(content)

def generate_plan(exa_key, groq_key, goal, duration, style):
    try:
        with st.spinner('Working on your personalized learning journey... ✨'):
            scheduler = LearningScheduler(exa_key, groq_key, 'prompt_template.txt')
            content = scheduler.create_learning_plan(goal, duration, style)
        return content, None
    except APIError as e:
        return None, str(e)

def create_pdf(content):
    st.success("🎉 Woohoo! Your learning plan is ready!")
    
    filename = f'studycraft_plan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    title = "StudyCraft Learning Plan"
    pdf = PDFDocument(filename, title)
    pdf.create_pdf(content)

    st.success(f"Your plan is safely tucked into a PDF: {filename}")
    with open(filename, "rb") as file:
        st.download_button(
            label="📥 Download Your Shiny New Learning Plan (PDF)",
            data=file,
            file_name=filename,
            mime="application/pdf"
        )
    
    st.markdown("*Remember: A journey of a thousand miles begins with a single click... or something like that. 🚶‍♂️💨*")

if __name__ == "__main__":
    main()