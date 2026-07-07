from Graph import graph
from User_query import GraphState
from langfuse_client import langfuse

while True:

    query = input("User : ")

    trace = langfuse.trace(
        name="HR Chatbot",
        input=query
    )

    state = GraphState(
        session_id="001",
        user_query=query
    )

    result = graph.invoke(state)

    print(result["final_answer"])

    trace.update(
        output=result["final_answer"]
    )