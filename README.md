# LLM Chat App

A lightweight Streamlit-based chat application for interacting with OpenAI or DeepSeek LLM models. Designed for private use, this app provides a simple interface for API-powered conversations with customizable authorization.

## Features

- **Multi-LLM Support**: Switch between OpenAI and DeepSeek models.
- **Secure Authentication**: Custom JSON-based user database with hashed passwords (not human-readable).
- **Private Use**: No exposed credentials, intended for personal/local deployment.
- **Streamlit UI**: Clean, interactive chat interface.

## Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   
2. Configure config.json with your API keys and user credentials.

3. Run:
    ```sh
    streamlit run app.py

⚠ Note: Keep the JSON auth file secure—this app is designed for trusted environments.
