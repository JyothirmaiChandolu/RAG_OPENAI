"""Session state initialization and management."""
import streamlit as st


def initialize_session_state():
    """Initialize all session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'models_loaded' not in st.session_state:
        st.session_state.models_loaded = False
    
    if 'processing_image' not in st.session_state:
        st.session_state.processing_image = False
    
    if 'uploaded_file_data' not in st.session_state:
        st.session_state.uploaded_file_data = None
    
    if 'memory' not in st.session_state:
        st.session_state.memory = None
    
    if 'show_uploader' not in st.session_state:
        st.session_state.show_uploader = False
    
    if 'user_input' not in st.session_state:
        st.session_state.user_input = None
    
    if 'session_logger' not in st.session_state:
        st.session_state.session_logger = None
    
    if 'cleanup_registered' not in st.session_state:
        st.session_state.cleanup_registered = False


def clear_chat_state():
    """Clear chat-related session state."""
    st.session_state.messages = []
    if st.session_state.memory:
        st.session_state.memory.clear()
    st.session_state.processing_image = False
    st.session_state.uploaded_file_data = None
    st.session_state.show_uploader = False