from datasets import Dataset

def dataset_bulider(
        question: str,
        Answer:str,
        contexts: list[str],
        ground_truth:str | None=None
):
    
    df=Dataset.from_dict({
        "question":[question],
        "response":[Answer],
        "retrieved_contexts":[[contexts]]
    })
    if ground_truth:
        df["Ground_truth"]=[ground_truth]

    return df