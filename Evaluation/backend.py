import asyncio
from Evaluation.Ragas_worker import RagasEvaluate

ragas=RagasEvaluate()

async def RagaEval(
        question:str,
        Answer:str,
        context:list[str],
        trace_id: str | None=None
):
    loop=asyncio.get_running_loop()
    results=await loop.run_in_executor(None, lambda: ragas.Evaluate(question=question,
                                                      Answer=Answer,
                                                      contexts=context,
                                           ))
    print("="*40)
    print("Ragas Evaluation")
    print("="*40)

    print(f"Answer relevency: {results['answer_relevancy']}")
    print(f"Faithfulness:{results['faithfulness']}")

    return results 