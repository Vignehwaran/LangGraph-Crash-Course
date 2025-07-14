from dotenv import load_dotenv
from langgraph.graph import StateGraph ,START,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode ,tools_condition
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from typing import Annotated
from langchain_tavily import TavilySearch
load_dotenv()

import os

from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

LLM=ChatGroq(
    model="llama3-70b-8192",
    temperature=1
)


# search=TavilySearch(max_results=2)

tools=[search]

llm=LLM.bind_tools(tools)


class State(TypedDict):
    messages:Annotated[list,add_messages]


def chattools(state:State):
    return{
        "messages":[llm.invoke(state["messages"])]
    }


graph_builder=StateGraph(State)

graph_builder.add_node("chat_with_tools",chattools)
graph_builder.add_node("tools",ToolNode(tools))
graph_builder.add_edge(START,"chat_with_tools")
graph_builder.add_conditional_edges("chat_with_tools",tools_condition)
graph_builder.add_edge("tools","chat_with_tools")


app=graph_builder.compile()




while True:
    query=input("here are : ")
    if query=="exist":
        break
    response=app.invoke({
        "messages":HumanMessage(content=query)
    })

    print(response["messages"][-1].content)