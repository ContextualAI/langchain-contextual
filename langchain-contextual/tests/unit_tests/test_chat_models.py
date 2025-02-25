"""Test chat model integration."""

from typing import Type

from langchain_contextual.chat_models import ChatContextual
from langchain_tests.unit_tests import ChatModelUnitTests


class TestChatContextualUnit(ChatModelUnitTests):
    @property
    def chat_model_class(self) -> Type[ChatContextual]:
        return ChatContextual

    @property
    def chat_model_params(self) -> dict:
        # These should be parameters used to initialize your integration for testing
        return {
            "model": "v1",
        }
