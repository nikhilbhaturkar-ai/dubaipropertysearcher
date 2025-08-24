import os
import streamlit as st
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

def get_llm_model():
    try:
        groq_api_key=os.getenv("GROQ_API_KEY")
        if groq_api_key=='':
            st.error("Unable to acquire the Groq API KEY")

        llm=ChatGroq(model="qwen/qwen3-32b")
    except Exception as e:
        raise ValueError(f"Error Ocuured With Exception : {e}")
    return llm
    