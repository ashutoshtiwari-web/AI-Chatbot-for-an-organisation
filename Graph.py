from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from User_query import GraphState

from agents.GaurdrailAgent import Gaurdrail_Agent

def gaurd_rail_node(state: GraphState):
    gaurdrail_Agent = Gaurdrail_Agent()
    category=gaurdrail_Agent.check(state.user_query)
    state.risk_category=category
    if category!="safe":
        state.is_safe=False
        print(f"Can not answer question around {category} category as it is not safe to answer and against the chatbot guidlines")
    else:
        state.is_safe=True

def route_after_gaurdrail(state: GraphState):
    if state.is_safe==True:
        return "intent"
    return "End"


from agents.intent_agent import ClassifyIntent

intent_agent = ClassifyIntent()

def intent_node(state: GraphState):

    state.intent = intent_agent.classify_intent(
        contents=state.context,
        query=state.user_query
    )

    return state
from agents.payroll_agent import PayrollAgent

payroll = PayrollAgent()

def payroll_node(state: GraphState):

    result = payroll.fetch_api_data(
        state.user_query
    )

    state.api_result = result

    return state  
from agents.benefits_agent import BenefitsAgent

benefits = BenefitsAgent()

def benefits_node(state: GraphState):

    result = benefits.fetch_api_data(
        state.user_query
    )

    state.api_result = result

    return state
from RAG import rag_chain, retriever

def rag_node(state: GraphState):

    docs = retriever.invoke(state.user_query)

    state.rag_documents = docs

    state.context = "\n".join(
        doc.page_content
        for doc in docs)
    return state
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3")

def generate_node(state: GraphState):

    prompt = f"""

Question:
{state.user_query}

Context:
{state.context}

API:
{state.api_result}

"""

    response = rag_chain.invoke(prompt)

    state.final_answer = response

    return state
def route(state: GraphState):

    if state.intent == "payroll":
        return "payroll"

    elif state.intent == "benefits":
        return "benefits"

    else:
        return "rag"

#graph
from langgraph.graph import StateGraph, END

workflow = StateGraph(GraphState)
workflow.add_node("gaurdrail", gaurd_rail_node)
workflow.add_node("intent", intent_node)

workflow.add_node("payroll", payroll_node)

workflow.add_node("benefits", benefits_node)

workflow.add_node("rag", rag_node)

workflow.add_node("generate", generate_node)      
workflow.set_entry_point("gaurdrail")


workflow.add_conditional_edges(
    "gaurdrail",
    route_after_gaurdrail,
    {
        "intent": "intent",
        "End": END
    }
)
workflow.add_conditional_edges(
    "intent",
    route,
    {
        "payroll": "payroll",
        "benefits": "benefits",
        "rag": "rag"
    }
)
workflow.add_edge(
    "payroll",
    "generate"
)
workflow.add_edge(
    "benefits",
    "generate"
)
workflow.add_edge(
    "rag",
    "generate"
)
workflow.add_edge(
    "generate",
    END
)

graph = workflow.compile()