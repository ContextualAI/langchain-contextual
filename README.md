# langchain-contextual

This package contains the LangChain integration with Contextual

## Installation

```bash
pip install -U langchain-contextual
```

And you should configure credentials by setting the following environment variables:

`CONTEXTUAL_AI_API_KEY` to your API key for Contextual AI

## Chat Models

`ChatContextual` class exposes chat models from Contextual.

```python
messages = [
    (
        "system",
        "You are a helpful assistant that uses all of the provided knowledge to answer the user's query to the best of your ability.",
    ),
    ("human", "What type of cats are there in the world and what are the types?"),
]

knowledge = [
    "There are 2 types of dogs in the world: good dogs and best dogs.",
    "There are 2 types of cats in the world: good cats and best cats.",
]

llm.invoke(messages, knowledge=knowledge)
```
