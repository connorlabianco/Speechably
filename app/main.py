import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    st.title("🗣️ Speechably")
    st.write("Creating confidence through user-driven feedback.")
    
    # Add your Streamlit components here
    st.write("Welcome to Speechably! Upload your video to get started.")

if __name__ == "__main__":
    main()
