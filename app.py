import streamlit as st
from langgraphagenticai.ui.streamlitui.load_ui import LoadMyStreamlitUI
from langgraphagenticai.LLMS import groqllm
from langgraphagenticai.LLMS.azureopenai import AZURE_LLM
from langgraphagenticai.graph import graph_builder
from langgraphagenticai.ui.uiconfigfile import Config
from langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.

    """
    ui=LoadMyStreamlitUI()
    ##Load UI
    st.set_page_config(page_title="Agentic AI Dubai Property Search", layout="wide")
    st.header("Agentic AI Dubai Property Search")
    st.session_state.IsFetchButtonClicked = False
    st.subheader("📰 Dubai Property Explorer ")
    if st.checkbox("🔍 Fetch property details",False):
        st.session_state.IsFetchButtonClicked = True

    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    # Text input for user message
    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            model=groqllm.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            ## Graph Builder
            try:
                #  graph=graph_builder.setup_graph(model)
                 print(user_message)
                #  DisplayResultStreamlit(graph,user_message).display_result_on_ui()
            except Exception as e:
                 st.error(f"Error: Graph set up failed- {e}")
                 return

        except Exception as e:
             st.error(f"Error: Graph set up failed- {e}")
             return   


if __name__=="__main__":
    load_langgraph_agenticai_app()