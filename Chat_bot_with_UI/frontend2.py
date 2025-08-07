import streamlit as st
from backend import chatbot
from langchain_core.messages import SystemMessage, HumanMessage
import uuid


#utility

def generate_id():
    thread_id=uuid.uuid4()
    return thread_id

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
         st.session_state['chat_thread'].append(thread_id)

def reset_chat():
    thread_id=generate_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['msg_history']=[]

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']


if 'msg_history' not in st.session_state:
    st.session_state['msg_history']=[]
    
if 'thread_id'  not in st.session_state:
    st.session_state['thread_id']=generate_id()
    
if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread']=[]

add_thread(st.session_state['thread_id']) 
      
#sidebar
    
st.sidebar.title('LANGGRAPH CHAT BOT')

 
if st.sidebar.button('New Chat'):
    reset_chat()


st.sidebar.header('My Conversation')

for thread_id in st.session_state['chat_thread'][::-1]:
     #st.sidebar.text(thread_id)
     if  st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        message=load_conversation(thread_id)
         
        temp_msg=[]
         
        for msg in message:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_msg.append({'role':role,'content':msg.content})
        st.session_state['msg_history']=temp_msg  
        
             

#main_ui
for msg in  st.session_state['msg_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input=st.chat_input('Type here')

CONFIG={'configurable':{'thread_id':st.session_state['thread_id']}}

if user_input:
    st.session_state['msg_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    stream=chatbot.stream(
    {'messages':[HumanMessage(content=user_input)]},
    config=CONFIG,
    stream_mode='messages'
     )
    
    ai_msg=st.write_stream(
        message_chunk.content for message_chunk,metadata in stream
    )
    st.session_state['msg_history'].append({'role':'assistant','content':ai_msg}) 
    
    
    
    

