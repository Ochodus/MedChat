import streamlit as st
import time
import argparse
import os
from streamlit_chat import message
from chat import MedChat


parser = argparse.ArgumentParser(description='Medical Chatbot')

parser.add_argument('--model', default='llama3:70b-instruct', help="Select the llm model.")
parser.add_argument('--translator', default=None, help="Select the translator.")
parser.add_argument('--max_q', default=None, help="Max number of question until get diagnosis.", type=int)
parser.add_argument('--prompt', default=None, help="Select prompt.")

try:
    args = parser.parse_args()
except SystemExit as e:
    os._exit(e.code)

st.title("MedChat V1.0")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "medChat" not in st.session_state:
    st.session_state.medChat = MedChat(llm=args.model, translator=args.translator, max_q=args.max_q, prompt=args.prompt)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
def response_generator(prompt):
    response = st.session_state.medChat(prompt)
    
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.05)
        

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})