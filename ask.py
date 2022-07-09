import sys
import logging
from pathlib import Path
from typing import Any, Dict, List
from haystack import Answer, Pipeline
import ray
from ray import serve
import yaml
from starlette.requests import Request
import asyncio


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


def spin_up():
    with open(CONFIG_PATH, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            with ray.init(address="auto", namespace="default"):
                serve.start(detached=True)
                QueryPipeline.options(name="game-of-thrones-q").deploy(config)
        except yaml.YAMLError as exc:
            print(exc)


# def ask():


if __name__ == "__main__":
    question = "Who plays Arya Stark?"
    if len(sys.argv) > 1:
        question = sys.argv[1]

    spin_up()

    # logger.info(f'Asking your question: "{question}"')
    # result =  ask(question)
    # documents: List[Answer] = result["answers"]

    # logger.info("The result is ready and it is:")
    # for answer in documents:
    #     print(f"The answer is: '{answer.answer}' with confidence {answer.score}")
    #     print(f"The context for the answer is: {answer.context}")
