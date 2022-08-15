import logging
import os
import ray
from pathlib import Path
from typing import Any, Dict, List
import httpx

import s3fs


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DATA_LOCAL_PATH = Path("./data/wiki_gameofthrones_txt")
DATA_GLOBAL_PATH = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip"


def prepare_data(local_path: Path, s3_url: str) -> List[Path]:
    if not local_path.exists():
        fs = s3fs.S3FileSystem()
        fs.download(s3_url, local_path)

    return [Path(f.name) for f in os.scandir(local_path)]


if __name__ == "__main__":
    logger.warning("Downloading data from S3")
    files = prepare_data(DATA_LOCAL_PATH, DATA_GLOBAL_PATH)

    logger.warning("Indexing files")
    for file in files:
        logger.warning(f"http://localhost:8000/game-of-thrones-index?file={file}")
        httpx.get(f"http://localhost:8000/game-of-thrones-index?file={file}")

    logger.warning("Indexing is over")
