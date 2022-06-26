# Local Haystack

The most simple code to run [Haystack](https://github.com/deepset-ai/haystack) locally

## Dependencies

You'll need [python](https://www.python.org/) and [docker-compose](https://docs.docker.com/compose/install/) installed.

## Start

We'll need a data storage. So first run:

```shell
docker-compose up -d
```

We also need to install the python dependencies:

```shell
pip install -r requirements.txt
```

Now we can execute our code with:

```shell
python ./run-haystack.py
```
