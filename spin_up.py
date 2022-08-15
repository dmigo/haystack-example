import os
import logging
from pathlib import Path
from typing import Any, Dict, List
from haystack import Answer, Pipeline
import ray
from ray import serve
import yaml
from starlette.requests import Request


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONFIG_PATH = Path("./config/sparse.yaml")
DATA_LOCAL_PATH = Path("./data/wiki_gameofthrones_txt")


@serve.deployment(
    _autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 10,
    },
    version="v1",
)
class QueryPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.query_pipeline = Pipeline.load_from_config(config, "query")

    async def __call__(self, request: Request):
        question = request.query_params["question"]
        result = self.query_pipeline.run(question)
        return result


@serve.deployment
class IndexingPipeline:
    def __init__(self, config: Dict[str, Any]):
        logger.info("Starting")
        self.indexing_pipeline = Pipeline.load_from_config(config, "indexing")

    @serve.batch(max_batch_size=100, batch_wait_timeout_s=60)
    async def index_batch(self, requests: List[Request]):
        file_paths = [
            os.path.join(DATA_LOCAL_PATH, request.query_params["file"])
            for request in requests
        ]
        self.indexing_pipeline.run(file_paths=file_paths)

    async def __call__(self, request: Request):
        await self.index_batch(request)


def spin_up():
    with open(CONFIG_PATH, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            with ray.init(address="auto", namespace="default"):
                serve.start(detached=True)
                QueryPipeline.options(name="game-of-thrones-query").deploy(config)
                IndexingPipeline.options(name="game-of-thrones-index").deploy(config)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    logger.warning("Starting pipelines")
    spin_up()
    logger.warning("Pipelines started")
