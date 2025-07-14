from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
#new thing
from langgraph.checkpoint.memory import MemorySaver


memory=MemorySaver()


llm=ChatGroq(
    model="llama3-70b-8192",
    temperature=1
)


class State(TypedDict):
    messages:Annotated[list,add_messages]


def chatbot(state:State):
    return {
        "messages":[llm.invoke(state["messages"])]
    }





bulider=StateGraph(State)


bulider.add_node("chatbot",chatbot)
bulider.add_edge(START,"chatbot")
bulider.add_edge("chatbot",END)



app=bulider.compile(checkpointer=memory)

config={
    "configurable":{
        "thread_id":"1"
    }
}


while True:
    query=input("you :")
    if query=="exit":
        break
    result=result=app.invoke({
        "messages":HumanMessage(content=query)
},config=config)
    

    print(f'AI messages {result["messages"][-1].content}')