"""Video background functionality."""
import os
import base64
import streamlit as st


def add_video_background(video_path):
    """Add a looping video background to the Streamlit app."""
    if not os.path.exists(video_path):
        return False
    
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode()
    
    video_html = f"""
    <style>
        #videoBackground {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            object-fit: fill;
        }}
    </style>
    <video autoplay loop muted playsinline id="videoBackground">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
    """
    st.markdown(video_html, unsafe_allow_html=True)
    return True


def add_fallback_background():
    """Add gradient fallback background if video is not available."""
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        }
    </style>
    """, unsafe_allow_html=True)