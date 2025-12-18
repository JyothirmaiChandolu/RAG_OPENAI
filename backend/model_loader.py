"""Model loading functions for embeddings, vector store, and LLM."""
import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from paddleocr import PaddleOCR

from config.settings import (
    EMBEDDING_MODEL_NAME,
    LLM_MODEL_NAME,
    OPENAI_API_KEY,
    FAISS_INDEX_PATH,
    TEMPERATURE,
    MAX_TOKENS
)

@st.cache_resource
def load_embeddings():
    """Load OpenAI embedding model."""
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL_NAME,
        openai_api_key=OPENAI_API_KEY
    )

@st.cache_resource
def load_vector_store():
    """Load FAISS vector store."""
    if not os.path.exists(FAISS_INDEX_PATH):
        st.error(f"⚠️ Vector store not found at {FAISS_INDEX_PATH}! Please run the notebook first.")
        return None
    
    embeddings = load_embeddings()
    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

@st.cache_resource
def load_llm():
    """Load OpenAI ChatGPT model."""
    return ChatOpenAI(
        model=LLM_MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        openai_api_key=OPENAI_API_KEY
    )

def load_ocr_model():
    """Load OCR model (cached in session state)."""
    if 'ocr_model' not in st.session_state or st.session_state.ocr_model is None:
        st.session_state.ocr_model = PaddleOCR(use_angle_cls=False, lang="en")
    return st.session_state.ocr_model