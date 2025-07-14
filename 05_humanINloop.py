#human in the loop
"""
correct the and validation of llm output

1. Aprove or reject
2.llm-->human-->accept or reject

"""

#method 1

from  langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import StateGraph, state ,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition
from langchain_core.messages import AIMessage,HumanMessage
from typing_extensions import Annotated
from typing import TypedDict

GENERATE_POST="generate_post"
GET_REVIEW_DECISION="get_review_decision"
POST="POST"
COLLECT_FEEDBACK="collect_feedback"


class State(TypedDict):
    messages:Annotated[list,add_messages]


llm=ChatGroq(
    model="llama3-70b-8192"
)

def generte_post(state:State): #why state:State typeHint chech
    return{
        "messages":[llm.invoke(state["messages"])] #state["messages"] extracting last human messages 	access the "messages" from the state dict
    }


def get_review_decision(state:State):
    post_content=state["messages"][-1].content
    print("/ curreent LinkedIN Post:\n") 
    print(post_content)
    print("\n")

    Decision=input("Post to LinkedIN? (yes/no)")

    if Decision.lower()=="yes":
        return POST
    else:
        return COLLECT_FEEDBACK
    

def post(state:State):
    final_post=state["messages"][-1].content
    print("Final Linked Post:\n")
    print(final_post)
    print("\n Post has beeb approved and is now on Linked!")


def collect_feedback(state:State):
    feedback=input("how can i improve this post?")
    return {
            "messages":[HumanMessage(content=feedback)]
    }


Bulider=StateGraph(State) #"I am building a LangGraph where every node will receive and return data matching the structure defined in State."


#create the nodes
Bulider.add_node(GENERATE_POST,generte_post)
Bulider.add_node(GET_REVIEW_DECISION,get_review_decision) #*****
Bulider.add_node(COLLECT_FEEDBACK,collect_feedback)
Bulider.add_node(POST,post)

#connecting the node using edges

Bulider.set_entry_point(GENERATE_POST)
Bulider.add_conditional_edges(GENERATE_POST,get_review_decision)
Bulider.add_edge(POST,END)
Bulider.add_edge(COLLECT_FEEDBACK,GENERATE_POST)

#another method
# builder.add_node("generate_post", generate_post)
# builder.add_node("get_review_decision", get_review_decision)
# builder.add_node("post", post)
# builder.add_node("collect_feedback", collect_feedback)

# # Define flow
# builder.set_entry_point("generate_post")
# builder.add_edge("generate_post", "get_review_decision")
# builder.add_conditional_edges(
#     "get_review_decision",
#     {
#         "post": "post",
#         "collect_feedback": "collect_feedback"
#     }
# )
# builder.add_edge("collect_feedback", "generate_post")
# builder.add_edge("post", END)


app=Bulider.compile() 


# response=app.invoke({
#     "messages":HumanMessage(content="wrtie the Linked in Post")
# })

from IPython.display import Image,display


display(Image(app.get_graph().draw_mermaid_png()))
