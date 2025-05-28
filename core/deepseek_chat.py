import streamlit as st
import os
from openai import OpenAI
from app_config import API_DEEPSEEK_KEY, BASE_DEEPSEEK_URL, DEEPSEEK_MODEL
from core.utils import cleanup_memory

def show():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Optional: Add system message
        st.session_state.messages.append({
            "role": "system",
            "content": "You are a helpful AI assistant."
        })

    # Get API key from environment variable
    api_key = API_DEEPSEEK_KEY

    # App title and description
    st.title("💬 DeepSeek Chat")
    st.caption("🚀 A conversational AI powered by DeepSeek")

    logout = st.toggle("Logout", value=False)
    if logout:
            logout_placeholder = st.empty()
            logout_placeholder.info("Logging out...")
            st.session_state.clear()
            cleanup_memory()
            st.rerun()

    # Display chat messages
    for message in st.session_state.messages[1:]:  # Skip system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Check for API key
    if not api_key:
        st.error("DEEPSEEK_API_KEY not found in environment variables")
        st.stop()

    # Chat input
    if prompt := st.chat_input("Message DeepSeek..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url=BASE_DEEPSEEK_URL
                )
                
                # Create chat completion with streaming
                stream = client.chat.completions.create(
                    model=DEEPSEEK_MODEL,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                    temperature=0.7  # Adjust for creativity
                )
                
                # Stream the response
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                full_response = "Sorry, I encountered an error processing your request."
                message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
