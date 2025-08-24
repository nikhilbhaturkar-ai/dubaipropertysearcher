import streamlit as st
import os
from langgraphagenticai.ui.uiconfigfile import Config

class LoadMyStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())
        st.session_state.IsFetchButtonClicked = False
        st.subheader("📰 Dubai Property Explorer ")
        if st.button("🔍 Fetch property details", use_container_width=True):
            st.session_state.IsFetchButtonClicked = True
        
        return self.user_controls