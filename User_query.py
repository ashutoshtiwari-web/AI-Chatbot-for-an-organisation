from typing import Optional, Dict, List
from langchain_core.documents import Document
from pydantic import BaseModel, Field

class GraphState(BaseModel):
    # Session information
    session_id: str

    # Original user question
    user_query: str

    # Intent detected by Intent Agent
    intent: Optional[str] = None

    # Which path LangGraph should take
    decision: Optional[str] = None

    # Response from Payroll/Benefits API
    api_result: Optional[Dict] = None

    # Documents retrieved from RAG
    rag_documents: list[Document] = Field(default_factory=list)

    # Combined context for LLM
    context: Optional[str] = ""

    # Final chatbot response
    final_answer: Optional[str] = None

    # Evaluation results (optional)
    evaluation: Optional[Dict] = None

    #for Guardrial Agent
    is_safe: bool = True

    risk_category: str = ""
