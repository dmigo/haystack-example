import sys
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


@serve.deployment
class QueryPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.query_pipelilne = Pipeline.load_from_config(config, "query")

    async def __call__(self, request: Request):
        body = await request.json()
        question = body.get("question", "Who plays Arya Stark?")
        result = self.query_pipelilne.run(question)
        return result


@serve.deployment
class IndexingPipeline:
    def __init__(self, config: Dict[str, Any]):
        logger.info("Starting")
        self.indexing_pipeline = Pipeline.load_from_config(config, "indexing")

    async def __call__(self, request: Request):
        body = await request.json()
        file_path = body.get("file_path")
        self.indexing_pipeline.run(file_paths=file_path)


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
    spin_up()
