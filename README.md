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

Now we need to index our data by semantics, this step might take quite some time if your computer doesn't have a GPU.

```shell
python ./index.py
```

Once the index is ready you can ask your questions as much as you want.

```shell
python ./ask.py
```
