from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
#from langchain_community.chat_models import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langgraph.graph import add_messages

class chat_state(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
    
    
model=ChatOllama(model='llama2')

def chat_node(state:chat_state):
    messages=state['messages']
    result=model.invoke(messages)
    return {'messages':[result]}

checkpointer=MemorySaver()
graph=StateGraph(chat_state)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)




