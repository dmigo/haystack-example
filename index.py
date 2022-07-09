import logging
import os
import ray
from pathlib import Path
from typing import Any, Dict, List
import yaml

import s3fs
from haystack import Pipeline


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DATA_LOCAL_PATH = Path("./data/wiki_gameofthrones_txt")
DATA_GLOBAL_PATH = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt1.zip"
CONFIG_PATH = Path("./config/sparse.yaml")


def get_file_paths(local_path: Path, s3_url: str) -> List[Path]:
    if not local_path.exists():
        logger.info("Downloading data from S3")
        fs = s3fs.S3FileSystem()
        fs.download(s3_url, local_path)

    return [Path(f.path) for f in os.scandir(local_path)]


@ray.remote
def run_indexing(config: Dict[str, Any]):
    logger.info("Starting")
    indexing_pipeline = Pipeline.load_from_yaml(CONFIG_PATH, "indexing")
    Pipeline.load_from_config(config, "indexing")
    file_paths = get_file_paths(DATA_LOCAL_PATH, DATA_GLOBAL_PATH)

    logger.info("Indexing")
    output = indexing_pipeline.run(file_paths=file_paths)
    logger.info("Indexed successfully")
    return output


if __name__ == "__main__":
    with open(CONFIG_PATH, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            with ray.init(address="auto", namespace="default") as ray_client:
                future = run_indexing.remote(config)
                output = ray_client.get(future)
                print(output)
        except yaml.YAMLError as exc:
            print(exc)
