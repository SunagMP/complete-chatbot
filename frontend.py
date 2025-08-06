import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage, AIMessage

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [{
        'role':'ai', 'message' : "Helpful assistant"
    }]

st.title("Chatbot")

for message in st.session_state['chat_history']:
     with st.chat_message(message['role']):
            st.write(message['message'])

config1 = {'configurable':{
    'thread_id' : "thread-1"
}}

query = st.chat_input("Type something")

if query:
    st.session_state['chat_history'].append(
        {'role' : 'human', 'message' : query}
    )
    with st.chat_message('human'):
        st.write(query)

    initial_state = {
        'message' : [HumanMessage(content=query)]
    }
    
    with st.chat_message('ai'):
        response = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                initial_state,
                config= config1,
                stream_mode= 'messages'
            )
        )
    
    st.session_state['chat_history'].append(
        {'role' : 'ai', 'message' : response}
    )