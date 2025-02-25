# langchain-contextual

This package contains the LangChain integration with Contextual

## Installation

```bash
pip install -U langchain-contextual
```

And you should configure credentials by setting the following environment variables:

`CONTEXTUAL_AI_API_KEY` to your API key for Contextual AI
`CONTEXTUAL_AI_BASE_URL` to your base_url for Contextual AI

## Chat Models

`ChatContextual` class exposes chat models from Contextual.

```python
from langchain_contextual import ChatContextual

llm = ChatContextual()
llm.invoke("Sing a ballad of LangChain.")
```
