import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

def get_llm():
    """Groq LLM initialization with updated supported model."""
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",  
        temperature=0.2,
    )

def get_chain(vector_store):
    """Creates a modern, state-of-the-art Conversational RAG chain using LCEL."""
    llm = get_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 1. Contextualize Question Prompt: Purani chat history ko dekh kar query ko rephrase karna
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # 2. Main System Prompt: Isse chatbot ek professional representative ki tarah baat karega
    system_prompt = (
    "You are 'Apex AI Assistant', an elite, helpful, and professional AI agent for Apex Coaching Classes.\n"
    "Your absolute and only identity is to represent Apex Coaching. Never use the word 'Veltro' in your responses, "
    "as that is strictly the internal technology provider and NOT the name of the institute.\n\n"
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, say that you don't know politely, don't try to make up an answer.\n"
    "Keep your answers concise, structured, and engaging. Use emojis appropriately to look professional.\n\n"
    "Context:\n{context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    # 3. Combine everything using modern chains
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain