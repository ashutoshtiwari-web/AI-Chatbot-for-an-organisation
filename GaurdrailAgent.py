from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

Gaurdrail_prompt="""You are an enterprise HR chatbot safety classifier.

Classify the user's query into exactly one category.

Categories:
- SAFE
- OUT_OF_SCOPE
- VIOLENCE
- SELF_HARM
- ILLEGAL
- HATE
- PROMPT_INJECTION

Return ONLY one word.

Example:
SAFE
"""
llm=ChatOllama(model="llama3",Temperature=0)

class Gaurdrail_Agent:
    def check(self,User_query:str):
        response=llm.invoke(
            [
                SystemMessage(content=Gaurdrail_prompt),
                HumanMessage(content=User_query)
            ]
        )
        category=response.content.strip().lower()
        return category
    
    