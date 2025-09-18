#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import datetime
import random

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def echo_response(user_input):
    """Generate echo response with some variety"""
    responses = [
        f"You said: '{user_input}'",
        f"I heard you say: {user_input}",
        f"Echo: {user_input}",
        f"Your message was: {user_input}",
        f"Repeating back: '{user_input}'"
    ]
    return random.choice(responses)

def main():
    st.set_page_config(
        page_title="Echo Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Simple Echo Chatbot")
    st.markdown("*This bot simply echoes back what you say*")
    
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
        
        st.info("This is a simple echo bot deployed on Azure!")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Display welcome message if no conversation yet
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown("Hello! I'm an echo bot. I'll repeat back whatever you say to me. Try sending me a message!")
    
    # Chat input
    if prompt := st.chat_input("Say something..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display echo response
        with st.chat_message("assistant"):
            response = echo_response(prompt)
            st.markdown(response)
        
        # Add assistant response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()


# In[6]:


## convert code to py file 
#import os 
#os.system("jupyter nbconvert --to script __test_azure_echo_bot.ipynb")


