# Local Haystack

The most simple code to run [Haystack](https://github.com/deepset-ai/haystack) locally

## Dependencies

You'll need [python](https://www.python.org/) and [docker-compose](https://docs.docker.com/compose/install/) installed.

## Start

We'll need a data storage. We have our `docker-compose` file with OpenSearch configured.

```shell
docker-compose up -d
```

We also need to install the python dependencies.

```shell
pip install -r requirements.txt
```

Now we need to prepare and index our data by semantics. We will use Game of Thrones wiki data. The data will be downloaded from a prepared archive and stored in opensearch. Depending on your internet connection and wether your machine has a GPU this step might take quite some time.

```shell
python index.py
```

Once the index is ready you can ask your questions as much as you want.

```shell
python ask.py "Who is the father of Arya Stark?"
```
