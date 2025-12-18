"""Configuration settings for the Kashmir Tourism Chatbot."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("API_KEY")

# Model Configuration
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
LLM_MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.4
MAX_TOKENS = 512

# Vector Store Configuration
FAISS_INDEX_PATH = "faiss_openai"
TOP_K_RETRIEVAL = 5
SIMILARITY_THRESHOLD = 0.2

# Memory Configuration
MEMORY_WINDOW_SIZE = 5

# Media Configuration
VIDEO_PATH = "/Users/jyothirmaichandolu/Desktop/RAGProject/188621-883402243_small.mp4"

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Kashmir Tourism Guide",
    "page_icon": "🏔️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Suggested Questions
SUGGESTED_QUESTIONS = [
    "Give me itinerary for 3 day stay in kashmir",
    "Tell me about adventure sports",
    "What pilgrimage sites are there?",
    "Best places for families?"
]