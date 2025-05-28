import streamlit as st
st.set_page_config(page_title="LLM Chat") 

from core import login, deepseek_chat, gpt_chat

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
#st.write(f"Running file: {os.path.basename(__file__)}")

if not st.session_state.logged_in:
    login.login_page()
else:
    if st.session_state.api_provider == "OpenAI":
        # Make OpenAI API calls
        gpt_chat.show()
    else:
        # Make DeepSeek API calls
        deepseek_chat.show()