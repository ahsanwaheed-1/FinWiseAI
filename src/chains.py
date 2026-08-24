from langchain_openai import ChatOpenAI
from src.prompts import NARRATIVE_CHAT_TEMPLATE
import os



def get_llm(api_key, model_name="gpt-5-nano"):
    """
    Initializes the ChatOpenAI model.
    """
    if not api_key:
        api_key = "dummy"
        
    return ChatOpenAI(
        model_name=model_name,
        temperature=0.7,
        openai_api_key=api_key
    )

def stream_recommendations(llm, inputs):
    """
    Generator function to stream LLM responses chunk by chunk.
    """
    # format_messages combines System and Human prompts with variables
    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(**inputs)
    
    # Use the model's stream method
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content
