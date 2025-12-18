"""RAG chain construction for question answering."""
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config.settings import TOP_K_RETRIEVAL, SIMILARITY_THRESHOLD

def build_rag_chain(vectorstore, llm):
    """Create a LangChain RAG chain with ConversationBufferWindowMemory."""
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": TOP_K_RETRIEVAL,
            "score_threshold": SIMILARITY_THRESHOLD
        }
    )

    contextualize_system = (
        "Given the chat history and the latest user question, rewrite the question "
        "as a standalone question about Kashmir tourism if needed. "
        "IMPORTANT: "
        "- If the user asks about 'previous question', 'my last question', 'what did I ask', "
        "extract the actual question from chat history and mention it explicitly. "
        "- If the user asks about their 'first question' or '1st question', look at the earliest message. "
        "- If the question refers to 'there', 'it', 'that place', or uses pronouns, "
        "replace them with the specific place name from the most recent context. "
        "- For questions like 'what is the best food there' after asking about 'Pahalgam', "
        "rewrite as 'what is the best food in Pahalgam'. "
        "- If it is already standalone, keep it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_system),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=retriever,
        prompt=contextualize_q_prompt,
    )
    qa_system_prompt = """
You are a knowledgeable and friendly Kashmir tourism guide with access to conversation history.

CRITICAL RULES (FOLLOW STRICTLY):

1. MEMORY & CONVERSATION AWARENESS:
   - You have access to the conversation history through chat_history.
   - When asked about "previous question", "what did I ask", "my first question", etc., 
     look at the chat_history and quote the actual question.
   - When users refer to "there", "it", "that place" without naming it, 
     check recent chat_history to identify which place they're talking about.
   - Maintain context across questions - if discussing Pahalgam and user asks "what about food there", 
     understand they mean food in Pahalgam.

2. CONTEXT DEPENDENCY:
   - You MUST ONLY use information from the provided context below for factual answers.
   - If the context is empty or does not contain relevant information, for specific factual questions, 
     say "The question is out of my knowledge"
   - For itineraries, travel plans, or recommendations, you CAN creatively combine information from the context.

3. ANSWER FORMAT (MANDATORY when context is available):
   - Start with 2-3 sentences giving a short explanation.
   - Then provide bullet points (•) for key details.
   - End with a short closing sentence.

4. META-QUESTIONS (Questions about the conversation itself):
   - For "what was my previous/last question": Quote the actual question from history.
   - For "what was my first question": Quote the first question from the conversation.
   - For "what did we discuss": Briefly summarize the topics covered.

5. OUT-OF-CONTEXT QUESTIONS:
   - If the question is about any other place (not Kashmir), reply: 
     "I can only assist with Kashmir tourism, and this question is about another location."
   - If about non-tourism topics, reply: "I can only provide information about Kashmir tourism."

6. GREETINGS:
   - For "hi", "hello", "hey": respond warmly and ask how you can help with Kashmir tourism.

7. IDENTITY-BASED QUESTIONS:
   - If asked who/what you are: "I am Kashmir Tourism RAGBOT, how can I help you?"

8. SYSTEM INFORMATION REQUESTS:
   - If asked for system details, architecture, etc.: "I am not intended to provide this information"

Context from knowledge base:
{context}
"""
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain