from Graph import graph
from User_query import GraphState
from langfuse_client import langfuse
from Evaluation.backend import RagaEval
import asyncio
from langfuse.langchain import CallbackHandler
cbh=CallbackHandler()

async def main():
    while True:

        query = input("User : ")

        state = GraphState(
            session_id="001",
            user_query=query
        )
        trace_id=cbh.last_trace_id
        result = graph.invoke(state,config={"callbacks":[cbh]})
        scores=await RagaEval(question=state.user_query,Answer=result['final_answer'],context=state.context,trace_id=trace_id)
        print(result["final_answer"])
        langfuse.create_score(trace_id=trace_id,
                            name='Answer Relevency',
                              value=scores["answer_relevency"])
        langfuse.create_score(trace_id=trace_id,
                               name="Faithfulness",
                               value=scores['faithfulness'])
if __name__=="__main__":
    asyncio.run(main())