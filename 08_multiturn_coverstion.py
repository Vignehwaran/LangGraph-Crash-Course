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
from langchain_core.messages import HumanMessage ,AIMessage,SystemMessage

#model initialization
llm=ChatGroq(
    model="llama-3.1-8b-instant", 
)

# Define the shared graph state
class State(TypedDict):
    linkedIN_topic: str
    generated_post: Annotated[list[str],add_messages]
    human_feedback: Annotated[list[str],add_messages]


def model(state:State):
    """here , we are using the LLM to generate a Linkedin post With human feedback incorporated"""

    print("model Generating the content")
    # linkin_topic=state["linkedIN_topic"]
    feedback=state["human_feedback"] if "human_feedback" in state else ['no geedback yet']

    prompt=f"""
    create the best linkin content {state["linkedIN_topic"]} if you have feed for huamn {feedback} if "human_feedback else" else " No feedback Yet"

"""
    response=llm.invoke([
        SystemMessage(content="you are an experpt LinkedIN"),
        HumanMessage(content=prompt)
    ])

    print("result:",response.content)

    return {
        "generated_post":[response.content]
    }

def Human_node(state:State):
    """
    
    Human Intervention Node loops back to model unless input done
    
    """

    user_feedback = interrupt(
        {
            "generated_post":state["generated_post"],
            "messages":"provide feedback or type  done to finish"
        }
    )
    print(f" human feedback :{user_feedback}")


    if user_feedback=="done":
        return Command(update={"human_feedback":state["human_feedback"]},goto="end_end")
    return Command(update={"human_feedback":state["human_feedback"]+[user_feedback]},goto="model")



def end_node(state:State):
    """findal Node"""
    print("Findal ouput",state["generated_post"])


graph=StateGraph(State)

graph.add_node("model",model)
graph.add_node("human_node",Human_node)
graph.add_node('end_node',end_node)


graph.add_edge(START,"model")

graph.add_edge('model',"human_node")

checkpointer = MemorySaver()
graph1 = graph.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": uuid.uuid4()}}
# Run until interrupt
likinin_topic=input('enter your linkedIN topic')
initital_state={
    "linkedIN_topic": likinin_topic,
    "generated_post": [],
    "human_feedback": [],
}

for chunk in graph1.stream(initital_state,config=config):
    for node_id , value in chunk.items():

        if (node_id=="__interrupt__"):
            while True:
                user_feedback=input("prove the feedback or type done to finish")


                graph1.invoke(Command(resume=user_feedback),config=config)

                if user_feedback.lower()=="done":
                    break
                


