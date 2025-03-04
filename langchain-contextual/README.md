# langchain-contextual

This package contains the LangChain integration with Contextual AI.

## Installation

```bash
pip install -U langchain-contextual
```

And you should configure credentials by setting the following environment variables:

`CONTEXTUAL_AI_API_KEY` to your API key for Contextual AI

## Chat Models

`ChatContextual` class exposes chat models from Contextual.

```python
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
