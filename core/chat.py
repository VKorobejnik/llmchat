import streamlit as st
from openai import OpenAI
from app_config import API_DEEPSEEK_KEY, BASE_DEEPSEEK_URL, DEEPSEEK_MODEL, API_OPENAI_KEY, OPENAI_MODEL 
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
    deepseek = True
    # Get API key from environment variable
    api_key = API_DEEPSEEK_KEY

    # App title and description
    if st.session_state.api_provider == "OpenAI":
        deepseek = False
        api_key = API_OPENAI_KEY
        st.title("💬 GPT-4o Chat")
        st.caption("🚀 A conversational AI powered by OpenAI GPT-4o")
    else:
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
        if deepseek:
            st.error("DEEPSEEK_API_KEY not found in environment variables")
            st.stop()
        else:
            st.error("OPENAI_API_KEY not found in environment variables.")
            st.stop()

    # Chat input
    start_message = "Message DeepSeek..."
    if not deepseek:
        start_message = "Message GPT-4o..."
    
    
    if prompt := st.chat_input(start_message, accept_file=True):
        # Handle both text and files
        user_content = []
        
        # Add text if present
        if prompt.text:
            user_content.append({"type": "text", "text": prompt.text})
            st.session_state.messages.append({"role": "user", "content": prompt.text})
            with st.chat_message("user"):
                st.markdown(prompt.text)

        # Add files if present
        if prompt.files:
            for uploaded_file in prompt.files:
                try:
                    # For text files
                    if uploaded_file.type == "text/plain":
                        # Read complete file content
                        file_content = str(uploaded_file.read(), "utf-8")
                        # Store complete content but show preview
                        content_to_store = f"File content: {file_content}"
                        
                        # Add to message history
                        st.session_state.messages.append({
                            "role": "user", 
                            "content": content_to_store,
                            "file_name": uploaded_file.name,  # Store metadata
                            "full_content": file_content    # Store complete content
                        })
                        
                        # Display preview to user
                        with st.chat_message("user"):
                            st.markdown(f"📄 Uploaded text file: {uploaded_file.name}")
                            with st.expander("View file content"):
                                st.text(file_content)  # Show complete content in expander
                    
                    # For images
                    elif uploaded_file.type.startswith('image/'):
                        content_to_store = f"Image file: {uploaded_file.name}"
                        st.session_state.messages.append({
                            "role": "user",
                            "content": content_to_store,
                            "file_name": uploaded_file.name,
                            "is_image": True
                        })
                        with st.chat_message("user"):
                            st.image(uploaded_file)
                            st.caption(f"🖼️ {uploaded_file.name}")
                    
                    # For other file types
                    else:
                        content_to_store = f"File: {uploaded_file.name} (Type: {uploaded_file.type})"
                        st.session_state.messages.append({
                            "role": "user",
                            "content": content_to_store,
                            "file_name": uploaded_file.name
                        })
                        with st.chat_message("user"):
                            st.markdown(f"📂 {uploaded_file.name}")
                            st.caption(f"File type: {uploaded_file.type}")
                
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
                    st.session_state.messages.append({
                        "role": "user", 
                        "content": f"Error processing file: {uploaded_file.name}"
                    })

        # Generate assistant response
        full_response = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                if deepseek:
                    client = OpenAI(api_key=api_key, base_url=BASE_DEEPSEEK_URL)
                    model = DEEPSEEK_MODEL
                else:
                    client = OpenAI(api_key=api_key)
                    model = OPENAI_MODEL
                
                # Prepare messages - send complete text content to API
                api_messages = []
                for m in st.session_state.messages:
                    if m["role"] == "system":
                        api_messages.append({"role": "system", "content": m["content"]})
                    elif "full_content" in m:  # For files with stored content
                        api_messages.append({"role": "user", "content": m["full_content"]})
                    elif isinstance(m["content"], str):
                        api_messages.append({"role": m["role"], "content": m["content"]})
                
                # Create chat completion
                stream = client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    stream=True,
                    temperature=0.7
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
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
