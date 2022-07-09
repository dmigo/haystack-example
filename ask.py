import sys
import logging
from pathlib import Path
from typing import List
from haystack import Answer, Pipeline


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONFIG_PATH = Path("./config/dense.yaml")


if __name__ == "__main__":
    question = "Who plays Arya Stark?"
    if len(sys.argv) > 1:
        question = sys.argv[1]

    logger.info("Starting")
    query_pipelilne = Pipeline.load_from_yaml(CONFIG_PATH, "query")

    logger.info(f'Asking your question: "{question}"')
    result = query_pipelilne.run(question)
    documents: List[Answer] = result["answers"]

    logger.info("The result is ready and it is:")
    for answer in documents:
        print(f"The answer is: '{answer.answer}' with confidence {answer.score}")
        print(f"The context for the answer is: {answer.context}")
