
# rag-astra-private

Based on RAG Chroma Private template from Langchain.

- Ref: https://github.com/langchain-ai/langchain/tree/master/templates/rag-chroma-private

Using AstraDB instead of Chroma for vectorstore - this is the only external API.

- Ref: https://python.langchain.com/docs/integrations/vectorstores/astradb
- Ref: https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/vectorstores/astradb.py
- Ref: https://github.com/datastax/astrapy

Using Llama2 through Llama.cpp for embeddings instead of GPT4All.

- Ref: https://python.langchain.com/docs/integrations/text_embedding/llamacpp
- Ref: https://github.com/ggerganov/llama.cpp
- Ref: https://ai.meta.com/resources/models-and-libraries/llama/
- Ref: https://ai.meta.com/resources/models-and-libraries/llama-downloads/

Using Ollama as the LLM Chat interface which is derived from the original.
- Ref: https://ollama.ai/
- Ref: https://github.com/jmorganca/ollama
- Ref: https://python.langchain.com/docs/integrations/chat/ollama

The vectorstore is created in `chain.py` and by default indexes a [popular blog posts on Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) for question-answering. 

# BELOW IS ALL TBD TBD TBD

## CODING TODO

- Prepare a separate step to populate the database (since timeout may happen due to slow embedding generation).
- Prepare a separate step to check whether the database is already populated. See: https://github.com/langchain-ai/langchain/tree/master/templates/rag-astradb

## Environment Setup

To set up the environment, you need to download Ollama. 

Follow the instructions [here](https://python.langchain.com/docs/integrations/chat/ollama). 

You can choose the desired LLM with Ollama. 

This template uses `llama2:7b-chat`, which can be accessed using `ollama pull llama2:7b-chat`.

There are many other options available [here](https://ollama.ai/library).

This package also uses Llama2 embeddings via [Llama2.cpp](https://python.langchain.com/docs/integrations/text_embedding/llamacpp). Once you have the model to use for embeddings and quantized it for local usage, take note of the path to the quantized .gguf and specify the environment variable LLAMA_MODEL_PATH.

You will also need access to [AstraDB](https://astra.datastax.com/signup) and create a Serverless AstraDB Vector database. Once you create the database, get the API endopoint and Application token and set up the environment variables ASTRA_DB_API_ENDPOINT and ASTRA_DB_APPLICATION_TOKEN.

## Usage

To use this package, you should first have the LangChain CLI installed:

```shell
pip install -U langchain-cli
```

To create a new LangChain project and install this as the only package, you can do:

```shell
langchain app new my-app --package rag-astradb-private
```

If you want to add this to an existing project, you can just run:

```shell
langchain app add rag-astradb-private
```

And add the following code to your `server.py` file:
```python
from rag_astradb_private import chain as rag_astradb_private_chain

add_routes(app, rag_astradb_private_chain, path="/rag-astradb-private")
```

(Optional) Let's now configure LangSmith. LangSmith will help us trace, monitor and debug LangChain applications. LangSmith is currently in private beta, you can sign up [here](https://smith.langchain.com/). If you don't have access, you can skip this section

```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

If you are inside this directory, then you can spin up a LangServe instance directly by:

```shell
langchain serve
```

This will start the FastAPI app with a server is running locally at 
[http://localhost:8000](http://localhost:8000)

We can see all templates at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
We can access the playground at [http://127.0.0.1:8000/rag-astradb-private/playground](http://127.0.0.1:8000/rag-astradb-private/playground)  

We can access the template from code with:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/rag-astradb-private")
```

The package will create and add documents to the vector database in `chain.py`. By default, it will load a popular blog post on agents. However, you can choose from a large number of document loaders [here](https://python.langchain.com/docs/integrations/document_loaders).
