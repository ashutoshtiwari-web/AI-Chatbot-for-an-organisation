from ragas import evaluate
from Evaluation.Dataset_bulider_for_raga import dataset_bulider
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper


from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    
)
metrics = [
    answer_relevancy,
    faithfulness,
    
]

llm=ChatOllama(model="llama3",temperature=0)
embeddings=OllamaEmbeddings(model="nomic-embed-text")
ragas_llm=LangchainLLMWrapper(llm)
ragas_embedding=LangchainEmbeddingsWrapper(embeddings)
class RagasEvaluate:
    
    def Evaluate(self,question:str,
                    Answer:str,
                    contexts:list[str],
                    ground_truth:str| None=None):
        dataset=dataset_bulider(question=question,
                    Answer=Answer,
                    contexts=contexts,
                    ground_truth=ground_truth)
        evaluation=evaluate(dataset=dataset,metrics=metrics,llm=ragas_llm,embeddings=ragas_embedding)

        return evaluation.to_pandas().to_dict("records")[0]

