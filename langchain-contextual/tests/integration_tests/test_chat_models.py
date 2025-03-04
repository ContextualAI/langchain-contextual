"""Test ChatContextual chat model."""

from typing import Type

import pytest
from langchain_tests.integration_tests import ChatModelIntegrationTests

from langchain_contextual.chat_models import ChatContextual


class TestChatContextualIntegration(ChatModelIntegrationTests):
    @property
    def chat_model_class(self) -> Type[ChatContextual]:
        return ChatContextual

    @property
    def chat_model_params(self) -> dict:
        # These should be parameters used to initialize your integration for testing
        return {
            "model": "v1",
        }

    # Override and skip the tests from the parent class
    @pytest.mark.xfail(reason="not implemented")
    def test_stream(self) -> None:
        return super().test_stream()

    @pytest.mark.xfail(reason="not implemented")
    def test_astream(self) -> None:
        return super().test_astream()

    @pytest.mark.xfail(reason="not implemented")
    def test_double_messages_conversation(self) -> None:
        return super().test_double_messages_conversation()

    @pytest.mark.xfail(reason="not implemented")
    def test_usage_metadata(self) -> None:
        return super().test_usage_metadata()

    @pytest.mark.xfail(reason="not implemented")
    def test_usage_metadata_streaming(self) -> None:
        return super().test_usage_metadata_streaming()
