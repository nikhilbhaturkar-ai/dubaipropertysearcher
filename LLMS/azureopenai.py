import os
import streamlit as st
from langchain_openai import AzureChatOpenAI

class AZURE_LLM:
    def __init__(self,user_contols_input):
        self.user_controls_input=user_contols_input

    def get_azure_llm_model(self):
        try:
            azure_api_key=self.user_controls_input["AZURE_OPEN_API_KEY"]
            selected_azure_model=self.user_controls_input["selected_model"]
            if azure_api_key=='' and os.environ["AZURE_OPEN_API_KEY"] =='':
                st.error("Please Enter the API KEY")

            llm=AzureChatOpenAI(api_key=azure_api_key,model=selected_azure_model)

        except Exception as e:
            raise ValueError(f"Error Ocuured With Exception : {e}")
        return llm

    