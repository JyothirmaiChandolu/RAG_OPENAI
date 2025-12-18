"""Custom CSS styling for the application."""
import streamlit as st


def apply_custom_styles():
    """Apply all custom CSS styles to the Streamlit app."""
    st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: transparent;
        padding-bottom: 120px;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 0.7rem;
        border-radius: 0.6rem;
        margin-bottom: 0.6rem;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        animation: fadeIn 0.3s ease-in;
        max-width: 70%;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        margin-right: 5%;
        font-size: 0.9rem;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .assistant-message {
        background: rgba(255, 255, 255, 0.95);
        color: #1f2937;
        margin-left: 5%;
        margin-right: auto;
        border: 1px solid rgba(102, 126, 234, 0.3);
        line-height: 1.6;
        font-size: 0.9rem;
    }
    
    .assistant-message strong {
        font-weight: 700;
        color: #4c1d95;
        font-size: 1.05em;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Title styling */
    h1 {
        color: white !important;
        font-weight: 700;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Snowfall Spinner styling */
    .snowfall-spinner {
        margin-left: 5%;
        margin-top: 10px;
        margin-bottom: 15px;
        background: rgba(102, 126, 234, 0.15);
        padding: 20px 40px;
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.4);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(15px);
        display: inline-block;
        max-width: 300px;
    }
    
    .snowfall-container {
        position: relative;
        width: 200px;
        height: 80px;
        overflow: hidden;
    }
    
    .thinking-text {
        text-align: center;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 10px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .snowflake {
        position: absolute;
        top: -10px;
        color: white;
        font-size: 1em;
        animation: fall linear infinite;
        opacity: 0.8;
    }
    
    @keyframes fall {
        0% {
            top: -10px;
            opacity: 0.8;
        }
        100% {
            top: 80px;
            opacity: 0.3;
        }
    }
    
    .snowflake:nth-child(1) { left: 10%; animation-duration: 2s; animation-delay: 0s; }
    .snowflake:nth-child(2) { left: 20%; animation-duration: 2.5s; animation-delay: 0.3s; }
    .snowflake:nth-child(3) { left: 30%; animation-duration: 2.2s; animation-delay: 0.6s; }
    .snowflake:nth-child(4) { left: 40%; animation-duration: 2.8s; animation-delay: 0.2s; }
    .snowflake:nth-child(5) { left: 50%; animation-duration: 2.3s; animation-delay: 0.5s; }
    .snowflake:nth-child(6) { left: 60%; animation-duration: 2.6s; animation-delay: 0.8s; }
    .snowflake:nth-child(7) { left: 70%; animation-duration: 2.4s; animation-delay: 0.4s; }
    .snowflake:nth-child(8) { left: 80%; animation-duration: 2.7s; animation-delay: 0.7s; }
    .snowflake:nth-child(9) { left: 90%; animation-duration: 2.9s; animation-delay: 0.1s; }
    
    /* Image processing container */
    .image-processing-container {
        margin-left: 5%;
        margin-top: 10px;
        margin-bottom: 15px;
        background: rgba(102, 126, 234, 0.15);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.4);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(15px);
        display: inline-block;
        max-width: 350px;
    }
    
    .image-processing-container img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .processing-status-text {
        color: white;
        font-size: 0.95rem;
        font-weight: 500;
        text-align: center;
        padding: 8px;
        background: rgba(102, 126, 234, 0.3);
        border-radius: 8px;
        margin-top: 8px;
    }
    
    /* FIXED CHAT INPUT AT BOTTOM */
    .fixed-chat-input {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(15, 23, 42, 0.98) 0%, rgba(15, 23, 42, 0.95) 50%, transparent 100%);
        padding: 20px;
        padding-left: calc(300px + 40px);
        padding-right: 40px;
        z-index: 999;
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="collapsedControl"] ~ .main .fixed-chat-input {
        padding-left: 40px;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 0.5rem;
        color: white !important;
    }
    
    /* Markdown text in main area */
    .main .stMarkdown {
        color: white;
    }
    
    /* Chat input specific styling */
    [data-testid="stChatInput"] {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stChatInput"] input {
        color: white !important;
    }
    
    /* Upload button in fixed container */
    .fixed-chat-input .stButton>button {
        height: 48px;
        width: 48px;
        border-radius: 50%;
        padding: 0;
        font-size: 1.2em;
        min-width: auto;
    }
</style>
""", unsafe_allow_html=True)