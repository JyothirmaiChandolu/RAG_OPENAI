# 🏔️ Kashmir Tourism RAG Chatbot

An intelligent, interactive tourism guide powered by Retrieval-Augmented Generation (RAG) technology. This AI-powered chatbot provides comprehensive information about Kashmir's attractions, culture, activities, and travel planning through natural conversations.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Module Documentation](#module-documentation)
- [How It Works](#how-it-works)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## 🎯 Overview

The Kashmir Tourism RAG Chatbot is an advanced conversational AI system that combines the power of Large Language Models (LLMs) with a curated knowledge base about Kashmir tourism. Built using Retrieval-Augmented Generation (RAG) architecture, it provides accurate, contextual, and helpful responses to user queries about:

- Tourist attractions and landmarks
- Adventure sports and activities
- Cultural sites and pilgrimage destinations
- Travel itineraries and planning
- Local cuisine and restaurants
- Accommodation recommendations
- Transportation and logistics
- Weather and best visiting times

### 🌟 Key Highlights

- **Conversational Memory**: Maintains context across multiple conversation turns
- **Image Processing**: Extract and summarize text from uploaded images (tickets, brochures, etc.)
- **Beautiful UI**: Stunning video background with smooth animations
- **Smart Retrieval**: Uses FAISS vector store for efficient similarity search
- **Context-Aware Responses**: Understands follow-up questions and pronouns
- **Modular Architecture**: Clean, maintainable, and scalable codebase

## ✨ Features

### Core Features

1. **RAG-Powered Q&A**
   - Retrieves relevant information from vector database
   - Generates contextual responses using GPT-3.5
   - Handles complex, multi-part questions

2. **Conversational Memory**
   - Remembers last 5 conversation turns
   - Handles follow-up questions naturally
   - Maintains topic context across queries

3. **Image Text Extraction**
   - Upload images (tickets, brochures, signs)
   - Automatic text extraction using OCR
   - AI-powered summarization of extracted content

4. **Smart Query Understanding**
   - Resolves pronouns and references
   - Handles "there", "it", "that place" contextually
   - Remembers previous questions when asked

5. **Interactive UI**
   - Video background for immersive experience
   - Animated loading states (snowfall effect)
   - Suggested questions for quick start
   - Mobile-responsive design

### User Experience Features

- ❄️ Snowfall animations during processing
- 🎨 Gradient chat bubbles with smooth transitions
- 📱 Fixed chat input at bottom for easy access
- 🖼️ Image preview during processing
- 💾 Session state persistence
- 🔄 Clear chat functionality
- 💡 Suggested questions sidebar

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                      (Streamlit App)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Application Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Session    │  │      UI      │  │   Routing    │     │
│  │    State     │  │  Components  │  │    Logic     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Service Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     OCR      │  │     Text     │  │    Memory    │     │
│  │   Service    │  │   Service    │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Backend Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Model     │  │  RAG Chain   │  │    Vector    │     │
│  │   Loader     │  │   Builder    │  │    Store     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   External Services                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   OpenAI     │  │    FAISS     │  │  PaddleOCR   │     │
│  │     API      │  │   Database   │  │    Engine    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### RAG Pipeline Flow

```
User Query
    │
    ▼
┌─────────────────────┐
│  Query Processing   │ ← Contextualize with chat history
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Vector Retrieval   │ ← Search FAISS index
│  (Top-K Similarity) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Context Assembly   │ ← Combine retrieved documents
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  LLM Generation     │ ← Generate response with context
│  (GPT-3.5)         │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Memory Update      │ ← Save to conversation buffer
└─────────┬───────────┘
          │
          ▼
    Response to User
```

### Image Processing Pipeline

```
Image Upload
    │
    ▼
┌─────────────────────┐
│  Preprocessing      │
│  - Resize           │
│  - CLAHE Enhancement│
│  - Bilateral Filter │
│  - Sharpening       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  OCR Extraction     │ ← PaddleOCR
│  (Text Recognition) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Text Summarization │ ← OpenAI GPT-3.5
└─────────┬───────────┘
          │
          ▼
    Display Result
```

## 📁 Project Structure

```
kashmir-tourism-chatbot/
│
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (API keys)
├── .gitignore                     # Git ignore file
├── README.md                      # This file
│
├── config/                        # Configuration module
│   ├── __init__.py
│   └── settings.py                # All configuration constants
│
├── backend/                       # Backend services
│   ├── __init__.py
│   ├── model_loader.py            # Model loading (embeddings, LLM, OCR)
│   ├── rag_chain.py               # RAG chain construction
│   └── memory_manager.py          # Conversation memory management
│
├── services/                      # Business logic services
│   ├── __init__.py
│   ├── ocr_service.py             # Image preprocessing and OCR
│   └── text_service.py            # Text summarization
│
├── ui/                           # User interface components
│   ├── __init__.py
│   ├── styles.py                  # CSS styling
│   ├── components.py              # Reusable UI components
│   └── background.py              # Video background setup
│
├── utils/                        # Utility functions
│   ├── __init__.py
│   ├── formatters.py              # Text formatting utilities
│   └── session_state.py           # Session state management
│
├── data/                         # Data directory (not in repo)
│   ├── faiss_openai/             # FAISS vector store
│   └── videos/                   # Background videos
│
└── notebooks/                    # Jupyter notebooks (optional)
    └── data_preparation.ipynb    # Notebook for preparing FAISS index
```

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit 1.28+ | Web UI framework |
| **LLM** | OpenAI GPT-3.5-turbo | Text generation |
| **Embeddings** | OpenAI text-embedding-ada-002 | Vector embeddings |
| **Vector DB** | FAISS | Similarity search |
| **OCR** | PaddleOCR | Text extraction from images |
| **Memory** | LangChain ConversationBufferWindowMemory | Conversation context |
| **Image Processing** | OpenCV | Image preprocessing |

### Python Libraries

```
streamlit>=1.28.0          # Web framework
python-dotenv>=1.0.0       # Environment variables
opencv-python>=4.8.0       # Image processing
numpy>=1.24.0              # Numerical operations
langchain>=0.1.0           # LLM orchestration
langchain-community>=0.0.13 # Community integrations
langchain-openai>=0.0.5    # OpenAI integration
faiss-cpu>=1.7.4           # Vector similarity search
paddleocr>=2.7.0           # OCR engine
paddlepaddle>=2.5.0        # PaddleOCR backend
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key
- 4GB+ RAM recommended
- Internet connection

### Step-by-Step Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/kashmir-tourism-chatbot.git
cd kashmir-tourism-chatbot
```

2. **Create Virtual Environment**

```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**

Create a `.env` file in the root directory:

```bash
# .env
API_KEY=your_openai_api_key_here
```

5. **Prepare FAISS Vector Store**

You need to create the FAISS index from your knowledge base:

```python
# This is typically done in a separate notebook or script
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load your documents
documents = [...]  # Your Kashmir tourism documents

# Create embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key="your_api_key"
)

# Create and save FAISS index
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("faiss_openai")
```

6. **Add Background Video (Optional)**

Place your video file in the project directory and update the path in `config/settings.py`:

```python
VIDEO_PATH = "path/to/your/video.mp4"
```

## ⚙️ Configuration

### Configuration File: `config/settings.py`

```python
# API Configuration
OPENAI_API_KEY = os.getenv("API_KEY")

# Model Settings
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
LLM_MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.4              # Lower = more focused, Higher = more creative
MAX_TOKENS = 512               # Maximum response length

# Vector Store Settings
FAISS_INDEX_PATH = "faiss_openai"
TOP_K_RETRIEVAL = 5            # Number of documents to retrieve
SIMILARITY_THRESHOLD = 0.2     # Minimum similarity score

# Memory Settings
MEMORY_WINDOW_SIZE = 5         # Number of conversation turns to remember

# Media Settings
VIDEO_PATH = "path/to/video.mp4"

# UI Settings
PAGE_CONFIG = {
    "page_title": "Kashmir Tourism Guide",
    "page_icon": "🏔️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
```

### Environment Variables

Create a `.env` file:

```bash
# OpenAI API Key (Required)
API_KEY=sk-...your-key-here...

# Optional: Custom paths
FAISS_INDEX_PATH=./data/faiss_openai
VIDEO_PATH=./data/videos/kashmir.mp4
```

## 🎮 Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Chatbot

1. **Ask Questions**
   - Type your question in the chat input at the bottom
   - Press Enter or click the send button

2. **Upload Images**
   - Click the upload button (⬆️) next to the chat input
   - Select an image (JPG, JPEG, PNG)
   - The bot will extract and summarize text from the image

3. **Use Suggested Questions**
   - Click any suggested question in the sidebar
   - The question will be automatically sent

4. **Clear Chat**
   - Click "Clear Chat" button in the sidebar
   - Resets conversation history and memory

### Example Conversations

**Basic Query:**
```
User: What are the best places to visit in Kashmir?

Bot: Kashmir offers numerous breathtaking destinations. Here are the must-visit places:
• Srinagar: The summer capital with Dal Lake and Mughal gardens
• Gulmarg: Famous for skiing and the world's highest golf course
• Pahalgam: Perfect for trekking and river rafting
• Sonamarg: Known as "Meadow of Gold" with stunning glaciers
...
```

**Follow-up Question:**
```
User: What about food there?

Bot: Pahalgam offers delicious Kashmiri cuisine. Popular dishes include:
• Rogan Josh: Aromatic lamb curry
• Gushtaba: Minced mutton balls in yogurt gravy
• Kahwa: Traditional green tea with saffron
...
```

**Itinerary Planning:**
```
User: Give me itinerary for 3 day stay in Kashmir

Bot: Here's a suggested 3-day Kashmir itinerary:

Day 1: Srinagar
• Morning: Arrive and check into houseboat on Dal Lake
• Afternoon: Visit Mughal Gardens (Shalimar, Nishat)
• Evening: Shikara ride on Dal Lake
...
```

## 📚 Module Documentation

### config/settings.py
**Purpose**: Centralized configuration management

**Key Components**:
- API keys and credentials
- Model parameters
- File paths
- UI configuration

**Usage**:
```python
from config.settings import OPENAI_API_KEY, LLM_MODEL_NAME
```

### backend/model_loader.py
**Purpose**: Load and cache AI models

**Functions**:
- `load_embeddings()`: Load OpenAI embedding model
- `load_vector_store()`: Load FAISS vector database
- `load_llm()`: Load ChatGPT model
- `load_ocr_model()`: Load PaddleOCR model

**Caching**: Uses `@st.cache_resource` for efficiency

**Usage**:
```python
from backend.model_loader import load_llm, load_vector_store

llm = load_llm()
vectorstore = load_vector_store()
```

### backend/rag_chain.py
**Purpose**: Construct RAG retrieval and generation pipeline

**Functions**:
- `build_rag_chain(vectorstore, llm)`: Creates complete RAG chain

**Features**:
- History-aware retrieval
- Context-aware question reformulation
- Structured prompting for consistent responses

**Usage**:
```python
from backend.rag_chain import build_rag_chain

rag_chain = build_rag_chain(vectorstore, llm)
response = rag_chain.invoke({"input": query, "chat_history": history})
```

### backend/memory_manager.py
**Purpose**: Manage conversation memory

**Functions**:
- `initialize_memory()`: Create memory buffer
- `save_to_memory(memory, input, output)`: Save conversation turn
- `get_chat_history(memory)`: Retrieve conversation history
- `clear_memory(memory)`: Reset conversation

**Usage**:
```python
from backend.memory_manager import initialize_memory, save_to_memory

memory = initialize_memory()
save_to_memory(memory, user_input, bot_response)
```

### services/ocr_service.py
**Purpose**: Image processing and text extraction

**Functions**:
- `preprocess_image(image_path)`: Enhance image quality
  - Resize, CLAHE enhancement, bilateral filtering, sharpening
- `extract_text_from_image(image_path)`: Extract text using OCR

**Image Processing Steps**:
1. Resize (1.5x scale)
2. CLAHE enhancement for contrast
3. Bilateral filter for noise reduction
4. Sharpening for edge enhancement
5. OCR prediction

**Usage**:
```python
from services.ocr_service import extract_text_from_image

text = extract_text_from_image("ticket.jpg")
```

### services/text_service.py
**Purpose**: Text summarization using LLM

**Functions**:
- `summarize_text_with_openai(text, llm)`: Generate concise summary

**Usage**:
```python
from services.text_service import summarize_text_with_openai

summary = summarize_text_with_openai(extracted_text, llm)
```

### ui/styles.py
**Purpose**: All CSS styling in one module

**Features**:
- Chat message bubbles
- Animations (snowfall, fade-in)
- Responsive layout
- Fixed chat input
- Sidebar styling

**Usage**:
```python
from ui.styles import apply_custom_styles

apply_custom_styles()
```

### ui/background.py
**Purpose**: Video background functionality

**Functions**:
- `add_video_background(video_path)`: Load and display video
- `add_fallback_background()`: Gradient background if video unavailable

**Usage**:
```python
from ui.background import add_video_background

success = add_video_background("video.mp4")
```

### ui/components.py
**Purpose**: Reusable UI components

**Functions**:
- `render_chat_message(role, content)`: Display chat bubble
- `render_snowfall_spinner()`: Animated loading indicator
- `render_loading_screen()`: Initial loading screen
- `render_image_processing(image_base64, status)`: Image preview with status
- `render_sidebar_status(...)`: System status display
- `render_suggested_questions(suggestions)`: Question buttons

**Usage**:
```python
from ui.components import render_chat_message, render_snowfall_spinner

render_chat_message("user", "Hello!")
render_snowfall_spinner()
```

### utils/formatters.py
**Purpose**: Text formatting utilities

**Functions**:
- `format_answer(answer)`: Convert markdown to HTML
  - Bold text → `<strong>` tags
  - Bullet points → HTML formatting
  - Line breaks → `<br>` tags

**Usage**:
```python
from utils.formatters import format_answer

formatted = format_answer("**Title**\n• Point 1\n• Point 2")
```

### utils/session_state.py
**Purpose**: Session state management

**Functions**:
- `initialize_session_state()`: Initialize all state variables
- `clear_chat_state()`: Reset chat-related state

**Session Variables**:
- `messages`: Chat history
- `models_loaded`: Model loading status
- `memory`: Conversation memory object
- `processing_image`: Image processing flag
- `uploaded_file_data`: Current uploaded file

**Usage**:
```python
from utils.session_state import initialize_session_state, clear_chat_state

initialize_session_state()
clear_chat_state()
```

## 🔍 How It Works

### RAG (Retrieval-Augmented Generation) Explained

1. **Document Ingestion**
   - Kashmir tourism documents are split into chunks
   - Each chunk is converted to vector embeddings using OpenAI's embedding model
   - Embeddings are stored in FAISS vector database

2. **Query Processing**
   - User query is analyzed with conversation history
   - Query is reformulated to be standalone if it contains pronouns or references
   - Query is converted to vector embedding

3. **Retrieval**
   - System searches FAISS index for similar document chunks
   - Top-K most relevant chunks are retrieved based on cosine similarity
   - Similarity threshold filters out irrelevant results

4. **Generation**
   - Retrieved chunks provide context to the LLM
   - LLM generates a response using both context and conversation history
   - Response follows structured format (intro → bullet points → conclusion)

5. **Memory Update**
   - New conversation turn is saved to memory buffer
   - Oldest turns are removed if buffer exceeds window size
   - Memory is used for future context-aware responses

### Image Processing Workflow

1. **Upload** → User uploads image
2. **Preprocessing** → Image enhancement for better OCR
   - Resize for optimal resolution
   - CLAHE for contrast enhancement
   - Bilateral filter for noise reduction
   - Sharpening for better edge detection
3. **OCR** → PaddleOCR extracts text
4. **Summarization** → GPT-3.5 creates concise summary
5. **Display** → Show extracted text and summary

### Memory Management

The chatbot uses a sliding window memory:
- Stores last 5 conversation turns
- Each turn includes user input and bot response
- Enables context-aware follow-up questions
- Automatic cleanup of oldest memories

## 🔌 API Reference

### Backend Functions

#### `load_embeddings()`
```python
def load_embeddings() -> OpenAIEmbeddings
```
**Returns**: OpenAI embeddings model instance  
**Cache**: Yes (`@st.cache_resource`)

#### `load_vector_store()`
```python
def load_vector_store() -> FAISS | None
```
**Returns**: FAISS vector store or None if not found  
**Cache**: Yes (`@st.cache_resource`)

#### `load_llm()`
```python
def load_llm() -> ChatOpenAI
```
**Returns**: ChatOpenAI model instance  
**Cache**: Yes (`@st.cache_resource`)

#### `build_rag_chain(vectorstore, llm)`
```python
def build_rag_chain(
    vectorstore: FAISS, 
    llm: ChatOpenAI
) -> RetrievalChain
```
**Parameters**:
- `vectorstore`: FAISS vector database
- `llm`: ChatOpenAI model

**Returns**: Complete RAG chain with history-aware retrieval

#### `initialize_memory()`
```python
def initialize_memory() -> ConversationBufferWindowMemory
```
**Returns**: Memory buffer instance (k=5)

### Service Functions

#### `extract_text_from_image(image_path)`
```python
def extract_text_from_image(image_path: str) -> str
```
**Parameters**: Path to image file  
**Returns**: Extracted text string  
**Raises**: `ValueError` if image cannot be read

#### `summarize_text_with_openai(text, llm)`
```python
def summarize_text_with_openai(text: str, llm: ChatOpenAI) -> str
```
**Parameters**:
- `text`: Text to summarize
- `llm`: ChatOpenAI model instance

**Returns**: Concise 2-3 sentence summary

### UI Functions

#### `render_chat_message(role, content)`
```python
def render_chat_message(role: str, content: str) -> None
```
**Parameters**:
- `role`: "user" or "assistant"
- `content`: Message HTML content

#### `apply_custom_styles()`
```python
def apply_custom_styles() -> None
```
Injects all CSS styling into Streamlit app.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Bugs

1. Check if bug already reported in [Issues](https://github.com/yourusername/kashmir-tourism-chatbot/issues)
2. Create detailed bug report with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information

### Suggesting Features

1. Open a [Feature Request](https://github.com/yourusername/kashmir-tourism-chatbot/issues/new)
2. Describe the feature and use case
3. Explain why it would be valuable

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/kashmir-tourism-chatbot.git

# Create branch
git checkout -b feature/my-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Make changes and test
streamlit run app.py

# Run tests (if available)
pytest tests/
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

## 🐛 Troubleshooting

### Common Issues

#### 1. "Vector store not found" Error

**Problem**: FAISS index doesn't exist

**Solution**:
```python
# Create FAISS index first
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key="your_key")
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("faiss_openai")
```

#### 2. "OpenAI API Key Error"

**Problem**: API key not set or invalid

**Solution**:
- Check `.env` file exists with `API_KEY=sk-...`
- Verify key is valid on OpenAI platform
- Ensure `.env` is in root directory

#### 3. "Module Not Found" Errors

**Problem**: Missing dependencies

**Solution**:
```bash
pip install -r requirements.txt
```

#### 4. Video Background Not Loading

**Problem**: Video file not found or incorrect path

**Solution**:
- Check `VIDEO_PATH` in `config/settings.py`
- Verify video file exists at specified path
- Use absolute path if relative path doesn't work
- Fallback gradient background will be used automatically

#### 5. OCR Not Working

**Problem**: PaddleOCR installation issues

**Solution**:
```bash
# Reinstall PaddleOCR and PaddlePaddle
pip uninstall paddleocr paddlepaddle -y
pip install paddlepaddle paddleocr
```

#### 6. Memory/Performance Issues

**Problem**: Application running slow

**Solution**:
- Reduce `MEMORY_WINDOW_SIZE` in config
- Decrease `TOP_K_RETRIEVAL` value
- Use `gpt-3.5-turbo` instead of `gpt-4`
- Clear browser cache and restart app

#### 7. Session State Errors

**Problem**: Session state variables not initialized

**Solution**:
- Ensure `initialize_session_state()` is called early in `main()`
- Clear browser cookies and restart app
- Check for typos in session state variable names

### Debug Mode

Enable debug logging:

```python
# Add to app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```