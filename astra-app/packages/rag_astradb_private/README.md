
# rag-astra-private

Based on RAG Chroma Private template from Langchain.

- Ref: https://github.com/langchain-ai/langchain/tree/master/templates/rag-chroma-private

We will be using RAGStack, a curated stack of open-source software for easing implementation of the RAG pattern in production-ready applications using Astra Vector DB or Apache Cassandra as a vector store. It includes all packages required to build production-ready RAG applications with LangChain and the Astra Vector database.

- Ref: https://www.datastax.com/products/ragstack
- Ref: https://docs.datastax.com/en/ragstack/docs/index.html

This is based on the Langchain Template framework so we also need Langserv which allows deployment of LangChain runnables and chains as a REST API,  and the Langchain CLI.

- Ref: https://www.langchain.com/langserve
- Ref: https://github.com/langchain-ai/langserve
- Ref: https://github.com/langchain-ai/langchain/blob/master/templates/README.md

We use AstraDB in place of the original Chroma for vectorstore.

- Ref: https://python.langchain.com/docs/integrations/vectorstores/astradb
- Ref: https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/vectorstores/astradb.py
- Ref: https://github.com/datastax/astrapy

We use Llama2 through Llama.cpp for embeddings instead of GPT4All.

- Ref: https://python.langchain.com/docs/integrations/text_embedding/llamacpp
- Ref: https://github.com/ggerganov/llama.cpp
- Ref: https://ai.meta.com/resources/models-and-libraries/llama/
- Ref: https://ai.meta.com/resources/models-and-libraries/llama-downloads/

We use Ollama as the LLM Chat interface which is derived from the original.

- Ref: https://ollama.ai/
- Ref: https://github.com/jmorganca/ollama
- Ref: https://python.langchain.com/docs/integrations/chat/ollama

We will also use the FastAPI framework to create APIs.

- Ref: https://fastapi.tiangolo.com/
- Ref: https://github.com/tiangolo/fastapi

We will access the FastAPI APIs through Uvicorn, an ASGI web server implementation for Python.

- Ref: https://www.uvicorn.org/
- Ref: https://github.com/encode/uvicorn

The vectorstore is created in `chain.py` and by default indexes a [popular blog posts on Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) for question-answering. 

## Environment Setup

To set up the environment, you need to download Ollama. 

Follow the instructions [here](https://python.langchain.com/docs/integrations/chat/ollama). 

You can choose the desired LLM with Ollama. 

This template uses `llama2:7b-chat`, which can be accessed using `ollama pull llama2:7b-chat`.

There are many other options available [here](https://ollama.ai/library).

This package also uses Llama2 embeddings via [Llama2.cpp](https://python.langchain.com/docs/integrations/text_embedding/llamacpp). Once you have the model to use for embeddings and quantized it for local usage, take note of the path to the quantized .gguf and specify the environment variable LLAMA_MODEL_PATH.

You will also need access to [AstraDB](https://astra.datastax.com/signup) and create a Serverless AstraDB Vector database. Once you create the database, get the API endopoint and Application token and set up the environment variables ASTRA_DB_API_ENDPOINT and ASTRA_DB_APPLICATION_TOKEN.

## Usage

To use this package, you will need to set up required Python packages. These are listed in the requirements.txt file.

```shell
pip3 install -r requirements.txt
```

To add the local package to your installation, go to the "packages" directory and run the following.

```shell
pip3 install -e rag_astradb_private
```

Log into Astra and create an Astra Serveless database.

Referencing the `.env.example` file, create a file that you can 'source' to set up the required environment variables.

(Optional) Let's now configure LangSmith. LangSmith will help us trace, monitor and debug LangChain applications. LangSmith is currently in private beta, you can sign up [here](https://smith.langchain.com/). If you don't have access, you can skip this section

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```
Once you have set up your environment variables, proceed.

If you are inside this directory, then you can spin up a LangServe instance directly by:

```shell
langchain serve
```

This will start the FastAPI app with a server is running locally at 
[http://localhost:8000](http://localhost:8000)

**Note that it will take a while it starts the first time since it will be retrieving the source text data, generate the embeddings (using your local Ollama installation, and then persisting that into a collection in Astra DB**

We can see all templates at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
We can access the playground at [http://127.0.0.1:8000/rag-astradb-private/playground](http://127.0.0.1:8000/rag-astradb-private/playground)  

We can access the template from code with:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-astradb-private")
```

The package will create and add documents to the vector database in `chain.py`. By default, it will load a popular blog post on agents. However, you can choose from a large number of document loaders [here](https://python.langchain.com/docs/integrations/document_loaders).
