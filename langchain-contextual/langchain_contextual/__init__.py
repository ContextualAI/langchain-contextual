from importlib import metadata

from langchain_contextual.chat_models import ChatContextual
from langchain_contextual.rerank import ContextualRerank

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = "0.1.0"
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "ContextualRerank",
    "ChatContextual",
    "__version__",
]
