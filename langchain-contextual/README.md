# langchain-contextual

This package contains the LangChain integration with Contextual AI.

Contextual AI is a platform that offers state-of-the-art Retrieval-Augmented Generation (RAG) technology for enterprise applications. Our platform and models helps innovative teams build production-ready AI applications that can process millions of pages of documents with exceptional accuracy.

This integration allows you to easily incorporate Contextual AI's Grounded Language Model and Reranker into your LangChain workflows.

## Features

This package provides access to two key components from Contextual AI:

- **Grounded Language Model (GLM)**: A specialized language model that grounds responses in provided knowledge, ensuring accurate and relevant outputs based on your data.
- **Contextual Reranker**: An advanced document reranking system that can prioritize the most relevant documents based on queries and custom instructions.

## Installation

```bash
pip install -U langchain-contextual
```

And you should configure credentials by setting the following environment variables:

`CONTEXTUAL_AI_API_KEY` to your API key for Contextual AI

## Using the Chat Models

The `ChatContextual` class exposes chat models like the Grounded Language Model (GLM) from Contextual.

```python
from langchain_contextual import ChatContextual

llm = ChatContextual(
    model="v1",
    max_new_tokens=1024,
    temperature=0,
    top_p=0.9,
)

# only "human" and "ai" are accepted types of messages
# message types must alternative between "human" and "ai" if more than one message
messages = [
    ("human", "What type of cats are there in the world and what are the types?"),
]

knowledge = [
    "There are 2 types of dogs in the world: good dogs and best dogs.",
    "There are 2 types of cats in the world: good cats and best cats.",
]

llm.invoke(messages, knowledge=knowledge)
```

## Using the Reranker

The `ContextualRerank` class exposes the reranker model from Contextual.

### Example Usage

```python
from langchain_core.documents import Document
from langchain_contextual import ContextualRerank

model = "ctxl-rerank-en-v1-instruct"

compressor = ContextualRerank(model=model)

query = "What is the current enterprise pricing for the RTX 5090 GPU for bulk orders?"

instruction = "Prioritize internal sales documents over market analysis reports. More recent documents should be weighted higher. Enterprise portal content supersedes distributor communications."

document_contents = [
    "Following detailed cost analysis and market research, we have implemented the following changes: AI training clusters will see a 15% uplift in raw compute performance, enterprise support packages are being restructured, and bulk procurement programs (100+ units) for the RTX 5090 Enterprise series will operate on a $2,899 baseline.",
    "Enterprise pricing for the RTX 5090 GPU bulk orders (100+ units) is currently set at $3,100-$3,300 per unit. This pricing for RTX 5090 enterprise bulk orders has been confirmed across all major distribution channels.",
    "RTX 5090 Enterprise GPU requires 450W TDP and 20% cooling overhead."
]

metadata = [
    {
        "Date": "January 15, 2025",
        "Source": "NVIDIA Enterprise Sales Portal",
        "Classification": "Internal Use Only"
    },
    {
        "Date": "11/30/2023",
        "Source": "TechAnalytics Research Group"
    },
    {
        "Date": "January 25, 2025",
        "Source": "NVIDIA Enterprise Sales Portal",
        "Classification": "Internal Use Only"
    }
]

documents = [
    Document(page_content=content, metadata=metadata[i])
    for i, content in enumerate(document_contents)
]
reranked_documents = compressor.compress_documents(
    query=query,
    instruction=instruction,
    documents=documents,
)
```