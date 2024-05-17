import streamlit as st
import time
import argparse
import os
import logging
from datetime import datetime
from streamlit_chat import message
from chat import MedChat


parser = argparse.ArgumentParser(description='Medical Chatbot')

parser.add_argument('--model', default='llama3:70b-instruct', help="Select the llm model.")
parser.add_argument('--translator', default=None, help="Select the translator.")
parser.add_argument('--max_q', default=None, help="Max number of question until get diagnosis.", type=int)
parser.add_argument('--prompt', default=None, help="Select prompt.")
parser.add_argument('--log_path', default=".", help="Set the path of logger")

START_GREETING = "안녕하세요! 저는 의료 챗봇 MedChat입니다. 어떤 불편한 증상을 겪고 계신가요?"

try:
    args = parser.parse_args()
except SystemExit as e:
    os._exit(e.code)

def get_logger(path="."):
    if not os.path.exists(f'{path}/logs'):
        os.makedirs(f'{path}/logs')
        
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    now = datetime.now()

    file_handler = logging.FileHandler(f"{path}/logs/{now.strftime('%Y%m%d_%H%M%S')}.log")
    for handler in logger.handlers: 
        logger.removeHandler(handler)
    logger.addHandler(file_handler)
    
    return logger

st.title("MedChat V1.0")

def init_conversation(force_init=False):
    if not 'logger' in st.session_state or force_init:
        st.session_state.logger = get_logger(args.log_path)
    
    if force_init:
        st.session_state.medChat.reset(logger=st.session_state.logger)
    elif not 'medChat' in st.session_state:
        st.session_state.medChat = MedChat(llm=args.model, translator=args.translator, max_q=args.max_q, prompt=args.prompt, logger=st.session_state.logger)

    # Initialize chat history
    if not 'messages' in st.session_state or force_init:
        st.session_state.messages = [{"role": "assistant", "content": START_GREETING}]
        st.session_state.logger.info(f"Med Chat: {START_GREETING}")
        with st.chat_message("assistant"):
            st.write_stream(response_generator(START_GREETING))

def response_generator(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.05)
        
init_conversation()

col1, col2 = st.columns([4, 1])

with col1:
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                    
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(st.session_state.medChat(prompt)))
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    # Utilize reset button
    reset_button_key = "reset_button"
    reset_button = st.button("Reset Chat", key=reset_button_key)
    if reset_button:
        init_conversation(force_init=True)