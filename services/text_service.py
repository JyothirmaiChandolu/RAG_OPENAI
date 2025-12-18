"""Text processing services including summarization."""
from langchain_core.messages import HumanMessage, SystemMessage


def summarize_text_with_openai(text, llm):
    """Summarize extracted text using OpenAI."""
    if not text or len(text.strip()) < 10:
        return "No meaningful text found in the image."
    
    messages = [
        SystemMessage(
            content=(
                "You are a helpful assistant that creates concise summaries. "
                "Provide a clear, brief summary of the given text in ONLY 2-3 sentences. "
                "Be concise and focus on the main message."
            )
        ),
        HumanMessage(content=f"Please summarize the following text:\n\n{text}")
    ]
    
    response = llm.invoke(messages)
    return response.content.strip()