import os
from dotenv import load_dotenv
load_dotenv()
Langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
Langfuse_private_key=os.getenv("LANGFUSE_SECRET_KEY")
Langfuse_host=os.getenv("LANGFUSE_HOST")
llm_model=os.getenv("LLM_Model")
