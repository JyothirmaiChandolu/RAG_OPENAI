"""Reusable UI components."""
import streamlit as st
from datetime import datetime


def render_chat_message(role, content):
    """Render a single chat message."""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">👤 You</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">🤖 Assistant</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)


def render_snowfall_spinner():
    """Render thinking spinner with snowfall animation."""
    st.markdown("""
    <div class="snowfall-spinner">
        <div class="thinking-text">🤔 Thinking...</div>
        <div class="snowfall-container">
            <div class="snowflake">❄</div>
            <div class="snowflake">❄</div>
            <div class="snowflake">❄</div>
            <div class="snowflake">❄</div>
            <div class="snowflake">❄</div>
            <div class="snowflake">❄</div>
            <div class="snowflake">❄</div>
            <div class="snowflake">❄</div>
            <div class="snowflake">❄</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_loading_screen():
    """Render initial loading screen."""
    st.markdown("""
    <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1000; width: 100%; display: flex; justify-content: center; align-items: center;">
        <div style="background: rgba(102, 126, 234, 0.15); padding: 30px 50px; border-radius: 15px; border: 2px solid rgba(102, 126, 234, 0.4); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); backdrop-filter: blur(15px);">
            <div style="text-align: center; color: white; font-size: 1.2rem; font-weight: 600; margin-bottom: 12px;">❄️ Loading models...</div>
            <div style="text-align: center; color: rgba(255,255,255,0.85); font-size: 0.9rem; margin-bottom: 15px;">This may take a moment</div>
            <div style="position: relative; width: 220px; height: 70px; overflow: hidden; margin: 0 auto;">
                <div class="snowflake">❄</div>
                <div class="snowflake">❄</div>
                <div class="snowflake">❄</div>
                <div class="snowflake">❄</div>
                <div class="snowflake">❄</div>
                <div class="snowflake">❄</div>
                <div class="snowflake">❄</div>
                <div class="snowflake">❄</div>
                <div class="snowflake">❄</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_image_processing(image_base64, status_text):
    """Render image processing status with preview."""
    st.markdown(f"""
    <div class="image-processing-container">
        <img src="data:image/png;base64,{image_base64}" alt="Processing">
        <div class="processing-status-text">{status_text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_status(models_loaded, message_count, memory_count):
    """Render sidebar status information."""
    st.subheader("📊 System Status")
    if models_loaded:
        st.success("✅ Models Loaded")
        st.info(f"💬 Messages: {message_count}")
        st.info(f"🧠 Memory: {memory_count} turns (max 5)")
    else:
        st.warning("⏳ Models not loaded")


def render_suggested_questions(suggestions):
    """Render suggested question buttons."""
    st.subheader("💡 Suggested Questions")
    for suggestion in suggestions:
        if st.button(suggestion, key=f"suggest_{suggestion}", use_container_width=True):
            st.session_state.user_input = suggestion