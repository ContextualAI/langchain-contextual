from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Dict, List, Optional, Sequence, Union

from langchain_core.callbacks.manager import Callbacks
from langchain_core.documents import BaseDocumentCompressor, Document
from langchain_core.utils import convert_to_secret_str, get_from_dict_or_env
from pydantic import Field, SecretStr, model_validator


class ContextualRerank(BaseDocumentCompressor):
    """Contextual AI Reranker model.

    Please make sure that you have `contextual-client` Python package installed.

    You will need to provide your api key in the init param or set the environment
    variable CONTEXTUAL_AI_API_KEY

    If you are using a custom `base_url` for Contextual AI, you will need to include
    it in the init param as well.

    Currently, only model `ctxl-rerank-en-v1-instruct` is supported."""

    client: Any = None
    """Contextual AI Client"""

    api_key: Optional[SecretStr] = Field(default=None)
    """Contextual AI API key."""

    top_n: Optional[int] = None
    """The number of top-ranked results to return"""

    model: str = "ctxl-rerank-en-v1-instruct"
    """The version of the reranker to use. Currently, we just have `ctxl-rerank-en-v1-instruct`."""

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        try:
            from contextual import ContextualAI
        except ImportError:
            raise ImportError(
                "Could not import contextual python package. "
                "Please install via the command `pip install contextual-client`."
            )
        else:
            values["api_key"] = convert_to_secret_str(
                get_from_dict_or_env(values, "api_key", "CONTEXTUAL_AI_API_KEY")
            )
            base_url = values.get("base_url", None)
            values["client"] = ContextualAI(
                api_key=values["api_key"].get_secret_value(),
                base_url=base_url,
            )
        return values

    def _doc_to_str(
        self,
        document: Union[str, Document, dict],
    ) -> str:
        if isinstance(document, Document):
            return document.page_content
        elif isinstance(document, dict):
            return json.dumps(document)
        else:
            return document

    def rerank(
        self,
        documents: Sequence[Union[str, Document, dict]],
        query: str,
        *,
        model: str = "ctxl-rerank-en-v1-instruct",
        top_n: Optional[int] = None,
        instruction: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Returns an ordered list of documents ordered by their relevance to the provided query.

        Args:
            documents: A sequence of documents to rerank.
            query: The query to use for reranking.
            model: The version of the reranker to use. Currently, we just have "ctxl-rerank-en-v1-instruct".
            top_n: The number of results to return. If None returns all results.
                Defaults to self.top_n.
            instruction: The instruction to be used for the reranker.
        """  # noqa: E501
        if len(documents) == 0:  # short-circuit empty documents list
            return []
        docs = [self._doc_to_str(doc) for doc in documents]
        metadata = [
            json.dumps(doc.metadata)
            if isinstance(doc, Document) and doc.metadata
            else ""
            for doc in documents
        ]
        model = model or self.model
        top_n = top_n if (top_n is None or top_n > 0) else self.top_n
        results = self.client.rerank.create(
            query=query,
            documents=docs,
            model=model,
            top_n=top_n,
            instruction=instruction,
            metadata=metadata,
        )
        result_dicts = []
        for res in results.results:
            result_dicts.append(
                {"index": res.index, "relevance_score": res.relevance_score}
            )
        return result_dicts

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[Callbacks] = None,
        model: str = "ctxl-rerank-en-v1-instruct",
        top_n: Optional[int] = None,
        instruction: Optional[str] = None,
    ) -> Sequence[Document]:
        """Compress documents using Contextual AI's rerank API.

        Args:
            documents: A sequence of documents to rerank.
            query: The query to use for reranking.
            model: The version of the reranker to use. Currently, we just have "ctxl-rerank-en-v1-instruct".
            top_n: The number of results to return. If None returns all results.
                Defaults to self.top_n.
            instruction: The instruction to be used for the reranker.
            callbacks: Callbacks to run during the compression process.

        Returns:
            A sequence of compressed documents.
        """
        compressed = []
        for res in self.rerank(
            documents,
            query,
            model=model,
            top_n=top_n,
            instruction=instruction,
        ):
            doc = documents[res["index"]]
            doc_copy = Document(doc.page_content, metadata=deepcopy(doc.metadata))
            doc_copy.metadata["relevance_score"] = res["relevance_score"]
            compressed.append(doc_copy)
        return compressed
