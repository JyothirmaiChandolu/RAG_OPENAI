"""Main Streamlit application for Kashmir Tourism Chatbot with Session Logging."""
import streamlit as st
import os
import base64
from datetime import datetime

from config.settings import PAGE_CONFIG, VIDEO_PATH, SUGGESTED_QUESTIONS
from backend.model_loader import load_vector_store, load_llm
from backend.rag_chain import build_rag_chain

from backend.memory_manager import (
    initialize_memory, 
    save_to_memory, 
    get_chat_history
)

from services.ocr_service import extract_text_from_image
from services.text_service import summarize_text_with_openai

from ui.styles import apply_custom_styles
from ui.background import add_video_background, add_fallback_background
from ui.components import (
    render_chat_message,
    render_snowfall_spinner,
    render_loading_screen,
    render_image_processing,
    render_sidebar_status,
    render_suggested_questions
)

from utils.session_state import initialize_session_state, clear_chat_state
from utils.formatters import format_answer

from backend.session_logger import (
    create_session_logger,
    set_session_logger,
    get_session_logger
)


# ==================== PAGE CONFIG ====================
st.set_page_config(**PAGE_CONFIG)

# ==================== INITIALIZE ====================
initialize_session_state()
apply_custom_styles()

if not add_video_background(VIDEO_PATH):
    st.warning(f"Video file not found at '{VIDEO_PATH}'. Using fallback background.")
    add_fallback_background()
if 'cleanup_registered' not in st.session_state:
    import atexit
    
    def cleanup_logger():
        """Cleanup logger on app exit"""
        session_logger = get_session_logger()
        if session_logger and not session_logger.stats.get("session_ended", False):
            session_logger.end_session()
            print("✅ Session logger closed on app shutdown")
    atexit.register(cleanup_logger)
    st.session_state.cleanup_registered = True


# ==================== MAIN APP ====================
def main():
    """Main application logic."""
    # Header
    st.title("🏔️Your Guide To Paradise")
    st.markdown(
        "<p style='color: rgba(255,255,255,0.9); font-size: 1.1rem;'>"
        "Ask me anything about Kashmir tourism, attractions, and travel information!"
        "</p>", 
        unsafe_allow_html=True
    )
    
    # Initialize memory
    memory = initialize_memory()
    
    # Initialize session logger (only once per session)
    if 'session_logger' not in st.session_state or st.session_state.session_logger is None:
        session_logger = create_session_logger()
        session_id = session_logger.start_session()
        st.session_state.session_logger = session_logger
        set_session_logger(session_logger)
        print(f"✅ Session logger initialized with ID: {session_id}")
    else:
        session_logger = st.session_state.session_logger
        set_session_logger(session_logger)
    
    # ==================== SIDEBAR ====================
    with st.sidebar:
        # Status (removed session info display)
        chat_history = get_chat_history(memory)
        render_sidebar_status(
            st.session_state.models_loaded,
            len(st.session_state.messages),
            len(chat_history) // 2
        )
        
        # Suggested questions
        render_suggested_questions(SUGGESTED_QUESTIONS)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat_state()
            st.rerun()
        
        # End session button
        if st.button("🔴 End Session", use_container_width=True):
            if session_logger and not session_logger.stats.get("session_ended", False):
                session_logger.end_session()
                st.session_state.session_logger = None
                set_session_logger(None)
                st.success("✅ Session ended and logs saved!")
            st.rerun()
    
    # ==================== LOAD MODELS ====================
    if not st.session_state.models_loaded:
        loading_placeholder = st.empty()
        with loading_placeholder:
            render_loading_screen()
        
        try:
            vectorstore = load_vector_store()
            
            if vectorstore is not None:
                llm = load_llm()
                
                st.session_state.vectorstore = vectorstore
                st.session_state.llm = llm
                st.session_state.rag_chain = build_rag_chain(vectorstore, llm)
                st.session_state.models_loaded = True
                
                st.success("✅ All models loaded successfully!")
                st.rerun()
            else:
                st.stop()
        except Exception as e:
            st.error(f"❌ Error loading models: {str(e)}")
            st.stop()
    
    # ==================== DISPLAY CHAT ====================
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            render_chat_message(message["role"], message["content"])
    
    # ==================== GENERATE RESPONSE ====================
    if (st.session_state.models_loaded and 
        len(st.session_state.messages) > 0 and 
        st.session_state.messages[-1]["role"] == "user" and
        not st.session_state.messages[-1]["content"].startswith("[🔎")):
        
        render_snowfall_spinner()
        
        try:
            user_query = st.session_state.messages[-1]["content"]
            rag_chain = st.session_state.rag_chain
            memory = st.session_state.memory
            
            # Handle greetings
            lower_q = user_query.strip().lower()
            if lower_q in ["hi", "hello", "hey", "hii", "hiii"]:
                assistant_response = "Hello! 😊 How can I help you with Kashmir tourism today?<br>"
                save_to_memory(memory, user_query, assistant_response)
                
                # Log successful query-response
                if session_logger:
                    session_logger.log_query_response(user_query, assistant_response, success=True)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                st.rerun()
            
            # Get chat history and invoke RAG
            chat_history = get_chat_history(memory)
            
            result = rag_chain.invoke({
                "input": user_query,
                "chat_history": chat_history
            })
            
            docs = result.get("context", [])
            assistant_response = result.get("answer", "")
            
            # Check if no context
            if (not docs or len(docs) == 0 or 
                "out of my knowledge" in assistant_response.lower()):
                assistant_response = "I don't have enough information to answer this question about Kashmir"
            
            # Save to memory
            save_to_memory(memory, user_query, assistant_response)
            
            # Log successful query-response with token counts
            if session_logger:
                session_logger.log_query_response(user_query, assistant_response, success=True)
            
            # Format answer
            if assistant_response != "I don't have enough information to answer this question about Kashmir":
                formatted_response = format_answer(assistant_response)
            else:
                formatted_response = assistant_response
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted_response,
                "timestamp": datetime.now()
            })
            
        except Exception as e:
            st.error(f"❌ Error generating response: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Sorry, I encountered an error. Please try again.",
                "timestamp": datetime.now()
            })
            # Don't log failed responses
        
        st.rerun()
    
    # ==================== CHAT INPUT ====================
    if st.session_state.models_loaded:
        st.markdown('<div class="fixed-chat-input">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([12, 1])
        
        with col1:
            user_input = st.chat_input("Ask me about Kashmir tourism or upload an image...")
        
        with col2:
            upload_clicked = st.button("⬆️", key="upload_btn", help="Upload Image")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # File uploader
        if upload_clicked or st.session_state.show_uploader:
            st.session_state.show_uploader = True
            uploaded_file = st.file_uploader(
                "Upload Image",
                type=["jpg", "jpeg", "png"],
                key="image_upload",
                label_visibility="collapsed"
            )
        else:
            uploaded_file = None
        
        # Handle suggested questions
        if st.session_state.user_input:
            user_input = st.session_state.user_input
            st.session_state.user_input = None
        
        # ==================== PROCESS IMAGE ====================
        if uploaded_file is not None and not st.session_state.processing_image:
            st.session_state.processing_image = True
            st.session_state.uploaded_file_data = uploaded_file
            
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": f"[🔎 Image: {uploaded_file.name}]",
                "timestamp": datetime.now()
            })
            
            # Save file
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Get image base64
            image_bytes = uploaded_file.getvalue()
            image_base64 = base64.b64encode(image_bytes).decode()
            
            processing_placeholder = st.empty()
            
            try:
                # Step 1: Extract text
                with processing_placeholder:
                    render_image_processing(image_base64, "⏳ Extracting text...")
                
                extracted_text = extract_text_from_image(temp_path)
                
                if extracted_text and len(extracted_text.strip()) > 10:
                    # Step 2: Summarize
                    with processing_placeholder:
                        render_image_processing(
                            image_base64, 
                            "✅ Text extracted<br>⏳ Generating summary..."
                        )
                    
                    llm = st.session_state.llm
                    summary = summarize_text_with_openai(extracted_text, llm)
                    
                    # Step 3: Complete
                    with processing_placeholder:
                        render_image_processing(image_base64, "✅ Complete!")
                    
                    response_content = (
                        f"<strong>📄 Extracted Text:</strong><br>{extracted_text}<br><br>"
                        f"<strong>📋 Summary:</strong><br>{summary}"
                    )
                    
                    # Log successful image processing
                    if session_logger:
                        query_text = f"Image uploaded: {uploaded_file.name}"
                        session_logger.log_query_response(query_text, response_content, success=True)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_content,
                        "timestamp": datetime.now()
                    })
                    
                    # Save to memory
                    save_to_memory(
                        memory,
                        f"Image uploaded: {uploaded_file.name}",
                        f"Extracted and summarized: {summary}"
                    )
                    
                    # Cleanup
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    st.session_state.processing_image = False
                    st.session_state.uploaded_file_data = None
                    st.session_state.show_uploader = False
                    
                    import time
                    time.sleep(1.5)
                    st.rerun()
                else:
                    processing_placeholder.empty()
                    st.error("❌ No text found")
                    
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    st.session_state.processing_image = False
                    st.session_state.uploaded_file_data = None
                    st.session_state.show_uploader = False
                    # Don't log failed attempts
                    
            except Exception as e:
                processing_placeholder.empty()
                st.error(f"❌ Error: {str(e)}")
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                st.session_state.processing_image = False
                st.session_state.uploaded_file_data = None
                st.session_state.show_uploader = False
                # Don't log failed attempts
        
        # ==================== HANDLE TEXT INPUT ====================
        if user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })
            st.rerun()
    else:
        st.info("⏳ Please wait for models to load...")


if __name__ == "__main__":
    main()