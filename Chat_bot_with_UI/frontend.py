import streamlit as st
from backend import chatbot
from langchain_core.messages import SystemMessage, HumanMessage

if 'msg_history' not in st.session_state:
    st.session_state['msg_history']=[]

for msg in  st.session_state['msg_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input=st.chat_input('Type here')

config={'configurable':{'thread_id':'1'}}

if user_input:
    st.session_state['msg_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
     

   
    
    stream=chatbot.stream(
    {'messages':[HumanMessage(content=user_input)]},
    config={'configurable':{'thread_id':'1'}},
    stream_mode='messages'
     )
    
    ai_msg=st.write_stream(
        message_chunk.content for message_chunk,metadata in stream
    )
    st.session_state['msg_history'].append({'role':'assistant','content':ai_msg}) 
    
    
    
    

