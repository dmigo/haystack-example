import logging
import os
from pathlib import Path
from haystack import Document, Pipeline, Answer
from haystack.utils import fetch_archive_from_http


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DATA_LOCAL_PATH = Path("./data/wiki_gameofthrones_txt")
DATA_GLOBAL_PATH = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip"
CONFIG_PATH = Path("./dense.yaml")


def download_data():
    doc_dir = DATA_LOCAL_PATH
    s3_url = DATA_GLOBAL_PATH
    fetch_archive_from_http(url=s3_url, output_dir=doc_dir)


def get_file_paths():
    if not DATA_LOCAL_PATH.exists():
        logger.info("Downloading data from S3")
        download_data()
    return [f.path for f in os.scandir(DATA_LOCAL_PATH)]


if __name__ == "__main__":
    logger.info("Starting")
    indexing_pipeline = Pipeline.load_from_yaml(CONFIG_PATH, "indexing")
    file_paths = get_file_paths()

    logger.info("Indexing")
    indexing_pipeline.run(file_paths=file_paths)
    logger.info("Indexed successfully")
