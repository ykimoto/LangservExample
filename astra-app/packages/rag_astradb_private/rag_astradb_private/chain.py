# Load
import os
from langchain.chat_models import ChatOllama
# from langchain.embeddings import GPT4AllEmbeddings
from langchain.embeddings import LlamaCppEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
# from langchain.vectorstores import Chroma
from langchain.vectorstores import AstraDB

from .populate_vector_store import populate

# Get env vars

token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
collection_name = os.getenv("ASTRA_DB_COLLECTION_NAME")
llama_modelpath = os.getenv("LLAMA_MODEL_PATH")

# Set models

embedding = LlamaCppEmbeddings(model_path=llama_modelpath)

vectorstore = AstraDB(
    embedding=embedding,
    collection_name=collection_name,
    token=token,
    api_endpoint=api_endpoint,
)

retriever = vectorstore.as_retriever()

# For demo reasons, let's ensure there are rows on the vector store.

inserted_lines = populate(vectorstore)
if inserted_lines:
    print(f"Done ({inserted_lines} lines inserted).")

# Prompt
# Optionally, pull from the Hub
# from langchain import hub
# prompt = hub.pull("rlm/rag-prompt")
# Or, define your own:
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# LLM
# Select the LLM that you downloaded
ollama_llm = "llama2:7b-chat"
model = ChatOllama(model=ollama_llm)

# RAG chain
chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)


# Add typing for input
class Question(BaseModel):
    __root__: str


chain = chain.with_types(input_type=Question)