#complete templet human Aprove or Rejected

from typing import Literal, TypedDict ,List
import uuid

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage ,AIMessage

#model initialization
llm=ChatGroq(
    model="llama-3.1-8b-instant", 
)

# Define the shared graph state
class State(TypedDict):
    messages : Annotated[List ,add_messages]


def generate_llm_output(state:State):
    return{
        "messages":[llm.invoke(state["messages"])]
    }


def human_approval(state:State):
    decision=interrupt({
        "question":"Do you approve the following output?",
         "messages":state["messages"]
    })

    if decision == "approve":
        return Command(goto="approved_path")
    else:
        return Command(goto="rejected_path")
    


def approved_node(state:State):
    print("approved path ouput")
    print(state["messages"])


def rejected_node(state:State):
    print("X reject the back to llm")

    prompt=f"""
      user want to modife the ouput {state["messages"]}

"""
    
    response=llm.invoke(prompt)
    return {
        "messages":AIMessage(content=response.content)
    }




builder = StateGraph(State)
builder.add_node("generate_llm_output", generate_llm_output)
builder.add_node("human_approval", human_approval)
builder.add_node("approved_path", approved_node)
builder.add_node("rejected_path", rejected_node)

builder.set_entry_point("generate_llm_output")
builder.add_edge("generate_llm_output", "human_approval")
builder.add_edge("approved_path", END)
builder.add_edge("rejected_path", END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Run until interrupt
config = {"configurable": {"thread_id": uuid.uuid4()}}
result = graph.invoke({"messages":HumanMessage(content="write the poem for love")}, config=config)
print(result["__interrupt__"])


find_output=graph.invoke(Command(resume="rejected"),config=config)

print(find_output["messages"][-1].content)



