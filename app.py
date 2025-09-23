#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import datetime
import os
from openai import OpenAI

print("I AM HERE________--____")

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_openai_response(user_input):
    """Get response from OpenAI API"""
    try:
        # Check if API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Error: OpenAI API key not found in environment variables"
        
        print(f"API Key found: {api_key[:10]}...")  # Print first 10 chars for debugging
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Make API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

def main():
    st.set_page_config(
        page_title="OpenAI Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 OpenAI Chatbot")
    st.markdown("*Powered by OpenAI GPT*")
    
    # Check API key status
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        st.success("✅ OpenAI API Key loaded successfully")
    else:
        st.error("❌ OpenAI API Key not found in environment variables")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.header("Controls")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.metric("Messages", len(st.session_state.messages))
        
        st.markdown(f"**Time:** {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        st.info("This chatbot uses OpenAI GPT deployed on Azure!")
        
        # Debug info
        st.markdown("**Debug Info:**")
        if api_key:
            st.text(f"API Key: {api_key[:10]}...")
        else:
            st.text("API Key: Not found")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Display welcome message if no conversation yet
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown("Hello! I'm an AI assistant powered by OpenAI. Ask me anything!")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display OpenAI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_openai_response(prompt)
            st.markdown(response)
        
        # Add assistant response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
