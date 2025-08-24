import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,graph,user_message):
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        if user_message:
            with st.spinner("Fetching and summarizing properties... ⏳"):
                result = graph.invoke({"messages": user_message})
                try:
                    # Display the markdown content in Streamlit
                    st.markdown(result, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"No results found")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")