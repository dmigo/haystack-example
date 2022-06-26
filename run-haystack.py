import logging
import os
from pathlib import Path
from haystack import Document, Pipeline, Answer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DATA_PATH = Path('./data/wiki_gameofthrones_txt')
CONFIG_PATH = Path('./sparse.yaml')


if __name__ == "__main__":
    logger.info("Starting...")
    indexing_pipeline = Pipeline.load_from_yaml(CONFIG_PATH, "indexing")
    query_pipelilne = Pipeline.load_from_yaml(CONFIG_PATH, "query")
    file_paths = [f.path for f in os.scandir(DATA_PATH)]

    logger.info("Indexing...")
    indexing_pipeline.run(
        file_paths=file_paths
    )
    logger.info("Asking...")
    result = query_pipelilne.run("Who is the father of Jon Snow?")

    logger.info(f"The result is ready and it is: {result}")
