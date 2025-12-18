"""Memory management for conversation history."""
import streamlit as st
from langchain.memory import ConversationBufferWindowMemory
from config.settings import MEMORY_WINDOW_SIZE


def initialize_memory():
    """Initialize ConversationBufferWindowMemory."""
    if st.session_state.memory is None:
        st.session_state.memory = ConversationBufferWindowMemory(
            k=MEMORY_WINDOW_SIZE,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    return st.session_state.memory


def save_to_memory(memory, user_input, assistant_response):
    """Save conversation turn to memory."""
    memory.save_context(
        {"input": user_input},
        {"answer": assistant_response}
    )


def get_chat_history(memory):
    """Get chat history from memory."""
    memory_vars = memory.load_memory_variables({})
    return memory_vars.get('chat_history', [])


def clear_memory(memory):
    """Clear conversation memory."""
    if memory:
        memory.clear()