from datasets import Dataset 
import os
from ragas import evaluate
from ragas.metrics import context_precision, faithfulness, answer_relevancy, LLMContextRecall
import os

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

def evaluate_ragas(query: str, answer: str,chunks, ground_truth):
    """
    Evaluate the generated answer with the given query and chunks using RAGAS evaluation metrics.

    Args:
        query (str): The question to be answered.
        answer (str): The generated answer.
        chunks (list): The list of relevant chunks.
        ground_truth (str): The ground truth answer.

    Returns:
        pd.DataFrame: A DataFrame containing the evaluation metrics.
    """
    data = {
        'question': [
            query
        ],
        'response': [
                answer
        ],
        'contexts': [
                chunks
        ],
        'ground_truth': [
            ground_truth
        ]
    }

    dataset = Dataset.from_dict(data)

    context_recall = LLMContextRecall()
    score = evaluate(dataset, metrics=[context_precision, faithfulness, answer_relevancy, context_recall])
    df = score.to_pandas()
    return df