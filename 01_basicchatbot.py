# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langgraph.graph import StateGraph,state,END
# from langgraph.graph.message import add_messages
# from typing_extensions import TypedDict
# from typing import Annotated
# from langchain_core.messages import HumanMessage ,SystemMessage

# #model
# LLm=ChatGroq(
#     model="llama3-70b-8192",
#     temperature=1
# )

# # response=LLm.invoke("what is weather now")
# # result=response.content
# # print(result)

# system_message=SystemMessage(content=f'tell about my three joke  about {state} in formate of 1,2,3 ')

# class State(TypedDict):
#     messages:Annotated[list,add_messages]


# def chatbot(state:State):
#     return {
#         "messages":[LLm.invoke(state["messages"]+[system_message])]
#     }


# Graph_builder=StateGraph(State)


# Graph_builder.add_node("chatbot",chatbot)
# Graph_builder.set_entry_point("chatbot")
# Graph_builder.add_edge("chatbot",END)


# app=Graph_builder.compile()


# while True:
#     query=input("query")
#     if query=="exit":
#         break
#     result=app.invoke(
        
#         {
#             "messages":HumanMessage(content=query)
#         }
#     )

#     print(result)


# Load environment variables from .env file
from dotenv import load_dotenv

# Import Groq model wrapper from LangChain
from langchain_groq import ChatGroq

# Import core graph building utilities from LangGraph
from langgraph.graph import StateGraph, state, END

# Utility to track chat history
from langgraph.graph.message import add_messages

# Type hint utilities
from typing_extensions import TypedDict
from typing import Annotated

# Message types for LLM interactions
from langchain_core.messages import HumanMessage, SystemMessage

# ----------------------------
# Initialize LLM with Groq's LLaMA3-70B model
LLm = ChatGroq(
    model="llama3-70b-8192",
    temperature=1
)

# Create a system message with joke instructions (dynamic state insertion here is wrong)
system_message = SystemMessage(content=f'tell about my three joke  about {state} in formate of 1,2,3')

# Define the shape of the state used in the graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Node function to invoke the LLM with history + system message
def chatbot(state: State):
    return {
        "messages": [LLm.invoke(state["messages"] + [system_message])]
    }

# Create a LangGraph builder object with the defined state
Graph_builder = StateGraph(State)

# Add the chatbot node to the graph
Graph_builder.add_node("chatbot", chatbot)

# Set chatbot as the entry point
Graph_builder.set_entry_point("chatbot")

# Define that chatbot leads directly to END
Graph_builder.add_edge("chatbot", END)

# Compile the graph into an executable app
app = Graph_builder.compile()

# Run a continuous input loop for user interaction
while True:
    query = input("query")  # Get user input
    if query == "exit":     # Exit condition
        break
    # Invoke the graph with new human message
    result = app.invoke({
        "messages": HumanMessage(content=query)
    })

    # Print the chatbot's response
    print(result)
