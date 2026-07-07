from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage , SystemMessage

llm_model="llama3"

with open('Prompts/intent_prompt.txt', 'r') as data:
    contents = data.read()

Intent_prompt=contents

class ClassifyIntent:
    def __init__(self):
        self.llm_model = "llama3"

    def classify_intent(self, contents, query) -> str:
        valid_intents = {"payroll", "benefits", "general"}
        llm = ChatOllama(model=self.llm_model, temperature=0)
        try:
            response = llm.invoke([
                SystemMessage(Intent_prompt),
                HumanMessage(query)])
            intent = response.content.strip().lower()

            if intent in valid_intents:
                 return intent
            else:
                return "genral"
        except Exception as e:
            print(f"Unable to classify intent: {e}")    
            return "genral"
    
