import logging
from pathlib import Path
from typing import List
from haystack import Pipeline, Answer


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONFIG_PATH = Path("./dense.yaml")


if __name__ == "__main__":
    question = "Who plays Arya Stark?"

    logger.info("Starting")
    query_pipelilne = Pipeline.load_from_yaml(CONFIG_PATH, "query")

    logger.info(f'Asking your question: "{question}"')
    result = query_pipelilne.run(question)
    documents: List[Answer] = result["documents"]

    logger.info("The result is ready and it is:")
    for answer in documents:
        print(answer.content)
