import logging
import os
from pathlib import Path
from typing import List

import s3fs
from haystack import Pipeline


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DATA_LOCAL_PATH = Path("./data/wiki_gameofthrones_txt")
DATA_GLOBAL_PATH = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip"
CONFIG_PATH = Path("./config/dense.yaml")


def get_file_paths(local_path: Path, s3_url: str) -> List[Path]:
    if not local_path.exists():
        logger.info("Downloading data from S3")
        fs = s3fs.S3FileSystem()
        fs.download(s3_url, local_path)

    return [Path(f.path) for f in os.scandir(local_path)]


if __name__ == "__main__":
    logger.info("Starting")
    indexing_pipeline = Pipeline.load_from_yaml(CONFIG_PATH, "indexing")
    file_paths = get_file_paths(DATA_LOCAL_PATH, DATA_GLOBAL_PATH)

    logger.info("Indexing")
    indexing_pipeline.run(file_paths=file_paths)
    logger.info("Indexed successfully")
